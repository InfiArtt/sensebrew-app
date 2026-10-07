import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/gestures.dart';
import 'dart:async';

class NativeTextField extends StatefulWidget {
  final String label;
  final String value;
  final bool isNumber;
  final bool isPassword;
  final double height;
  final ValueChanged<String>? onChanged;
  final VoidCallback? onDone;

  const NativeTextField({
    super.key,
    required this.label,
    required this.value,
    this.isNumber = false,
    this.isPassword = false,
    this.height = 56,
    this.onChanged,
    this.onDone,
  });

  @override
  State<NativeTextField> createState() => _NativeTextFieldState();
}

class _NativeTextFieldState extends State<NativeTextField> {
  MethodChannel? _channel;
  String _lastValue = '';
  final FocusNode _focusNode = FocusNode();
  bool _isNativeActive = false;

  @override
  void initState() {
    super.initState();
    _lastValue = widget.value;
  }

  @override
  void didUpdateWidget(covariant NativeTextField oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.value != _lastValue) {
      _lastValue = widget.value;
      _channel?.invokeMethod('setValue', {'value': widget.value});
    }
    if (widget.isPassword != oldWidget.isPassword) {
      _channel?.invokeMethod('setIsPassword', {'isPassword': widget.isPassword});
    }
  }

  @override
  void dispose() {
    _focusNode.dispose();
    super.dispose();
  }

  void _scrollToEnsureVisible() {
    if (mounted) {
      Scrollable.ensureVisible(
        context,
        alignment: 0.5,
        duration: const Duration(milliseconds: 300),
      );
    }
  }

  void _activateNativeEditText() {
    // 1. Remove ExcludeSemantics so Flutter registers the PlatformView
    // in the Accessibility Tree via AccessibilityViewEmbedder.
    setState(() {
      _isNativeActive = true;
    });

    // 2. Wait slightly for the Flutter framework to flush semantics
    // before asking Kotlin to send TYPE_VIEW_FOCUSED. If we don't wait,
    // the event might fire before the node mapping exists.
    Timer(const Duration(milliseconds: 100), () {
      _channel?.invokeMethod('requestFocus');
      _focusNode.requestFocus();
      _scrollToEnsureVisible();
    });
  }

  @override
  Widget build(BuildContext context) {
    if (defaultTargetPlatform != TargetPlatform.android) {
      return SizedBox(
        height: widget.height,
        child: TextField(
          decoration: InputDecoration(
            labelText: widget.label,
            border: const OutlineInputBorder(),
          ),
          obscureText: widget.isPassword,
          keyboardType: widget.isNumber ? TextInputType.number : TextInputType.text,
          onChanged: widget.onChanged,
        ),
      );
    }

    final Map<String, dynamic> creationParams = <String, dynamic>{
      'label': widget.label,
      'value': widget.value,
      'type': widget.isNumber ? 'number' : 'text',
      'isPassword': widget.isPassword,
    };

    final platformView = Focus(
      focusNode: _focusNode,
      child: PlatformViewLink(
        viewType: 'sensebrew/native_textfield',
        surfaceFactory: (context, controller) {
          return AndroidViewSurface(
            controller: controller as AndroidViewController,
            gestureRecognizers: const <Factory<OneSequenceGestureRecognizer>>{},
            hitTestBehavior: PlatformViewHitTestBehavior.opaque,
          );
        },
        onCreatePlatformView: (params) {
          final view = PlatformViewsService.initExpensiveAndroidView(
            id: params.id,
            viewType: 'sensebrew/native_textfield',
            layoutDirection: TextDirection.ltr,
            creationParams: creationParams,
            creationParamsCodec: const StandardMessageCodec(),
            onFocus: () {
              params.onFocusChanged(true);
              if (!_isNativeActive) {
                setState(() { _isNativeActive = true; });
              }
              _focusNode.requestFocus();
              _scrollToEnsureVisible();
            },
          );

          view.addOnPlatformViewCreatedListener((id) {
            params.onPlatformViewCreated(id);
            _channel = MethodChannel('sensebrew/nativetf_$id');
            _channel!.setMethodCallHandler((call) async {
              if (call.method == 'onChanged') {
                final val = call.arguments as String;
                setState(() {
                  _lastValue = val;
                });
                widget.onChanged?.call(val);
              } else if (call.method == 'onDone') {
                widget.onDone?.call();
              } else if (call.method == 'onFocused') {
                if (!_isNativeActive) {
                  setState(() { _isNativeActive = true; });
                }
                _focusNode.requestFocus();
                Future.delayed(const Duration(milliseconds: 300), _scrollToEnsureVisible);
              } else if (call.method == 'onFocusLost') {
                // When focus is lost, re-exclude the platform view
                // from the semantics tree so the proxy can take over navigation.
                if (_isNativeActive) {
                  setState(() { _isNativeActive = false; });
                }
              } else if (call.method == 'onAccessibilityFocused') {
                _scrollToEnsureVisible();
              }
            });
          });

          view.create();
          return view;
        },
      ),
    );

    return SizedBox(
      height: widget.height,
      child: Stack(
        children: [
          // 1. The Native View
          // Excluded from semantics when NOT active, so TalkBack skips it during swipe.
          // Included when active, so AccessibilityBridge officially maps it and native cursor controls work.
          ExcludeSemantics(
            excluding: !_isNativeActive,
            child: platformView,
          ),
          
          // 2. The Proxy Overlay
          // Active ONLY when _isNativeActive is false. It intercepts swipe navigation
          // and double-taps.
          if (!_isNativeActive)
            Positioned.fill(
              child: Semantics(
                textField: true,
                label: widget.label,
                value: _lastValue,
                onTap: _activateNativeEditText,
                child: GestureDetector(
                  onTap: _activateNativeEditText,
                  behavior: HitTestBehavior.opaque,
                  excludeFromSemantics: true,
                  child: const SizedBox.expand(), // Transparent overlay to catch touch
                ),
              ),
            ),
        ],
      ),
    );
  }
}
