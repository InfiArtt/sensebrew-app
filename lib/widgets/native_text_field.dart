import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/gestures.dart';

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
      debugPrint("NativeTextField: Scrolling to middle for ${widget.label}");
      Scrollable.ensureVisible(
        context,
        alignment: 0.5,
        duration: const Duration(milliseconds: 300),
      );
    }
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

    return SizedBox(
      height: widget.height,
      child: Focus(
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
                  _lastValue = val;
                  widget.onChanged?.call(val);
                } else if (call.method == 'onDone') {
                  widget.onDone?.call();
                } else if (call.method == 'onFocused') {
                  _focusNode.requestFocus();
                  // Give keyboard time to animate up before scrolling
                  Future.delayed(const Duration(milliseconds: 300), _scrollToEnsureVisible);
                } else if (call.method == 'onAccessibilityFocused') {
                  // Always scroll to center to prevent TalkBack getting stuck at bottom
                  _scrollToEnsureVisible();
                }
              });
            });

            view.create();
            return view;
          },
        ),
      ),
    );
  }
}
