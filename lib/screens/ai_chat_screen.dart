import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:record/record.dart';
import 'package:path_provider/path_provider.dart';
import '../core/recipe.dart';
import '../core/settings_state.dart';
import '../core/ai_service.dart';
import '../core/app_strings.dart';
import '../widgets/native_text_field.dart';


class AiChatScreen extends StatefulWidget {
  final Recipe? initialRecipe;
  const AiChatScreen({super.key, this.initialRecipe});

  @override
  State<AiChatScreen> createState() => _AiChatScreenState();
}

class _AiChatScreenState extends State<AiChatScreen> {
  final _textController = TextEditingController();
  final _audioRecorder = AudioRecorder();
  
  bool _isRecording = false;
  bool _isLoading = false;
  
  List<Map<String, dynamic>> _messages = [];
  Recipe? _currentDraft;

  @override
  void initState() {
    super.initState();
    final lang = Provider.of<SettingsState>(context, listen: false).appLanguage;
    _messages.add({
      'role': 'ai',
      'text': widget.initialRecipe != null 
          ? AppStrings.str(lang, 'ai_greet_edit', [widget.initialRecipe!.name])
          : AppStrings.str(lang, 'ai_greet_new'),
    });
    _currentDraft = widget.initialRecipe;
  }

  @override
  void dispose() {
    _textController.dispose();
    _audioRecorder.dispose();
    super.dispose();
  }

  Future<void> _startRecording() async {
    try {
      if (await _audioRecorder.hasPermission()) {
        final dir = await getTemporaryDirectory();
        final path = '${dir.path}/temp_voice_note.m4a';
        
        await _audioRecorder.start(
          const RecordConfig(encoder: AudioEncoder.aacLc),
          path: path,
        );
        
        setState(() {
          _isRecording = true;
        });
      }
    } catch (e) {
      print("Recording error: $e");
    }
  }

  Future<void> _stopRecording() async {
    try {
      final path = await _audioRecorder.stop();
      setState(() {
        _isRecording = false;
      });
      
      if (path != null) {
        setState(() {
          final lang = Provider.of<SettingsState>(context, listen: false).appLanguage;
        _messages.add({'role': 'user', 'text': AppStrings.str(lang, 'ai_voice_note')});
          _isLoading = true;
        });
        
        final bytes = await File(path).readAsBytes();
        final base64Audio = base64Encode(bytes);
        
        File(path).delete().catchError((e) => print(e));

        await _processAiRequest(audioBase64: base64Audio);
      }
    } catch (e) {
      print("Stop recording error: $e");
    }
  }

  Future<void> _sendText() async {
    final text = _textController.text.trim();
    if (text.isEmpty) return;
    
    _textController.clear();
    setState(() {
      _messages.add({'role': 'user', 'text': text});
      _isLoading = true;
    });
    
    await _processAiRequest(prompt: text);
  }

  Future<void> _processAiRequest({String? prompt, String? audioBase64}) async {
    final settings = Provider.of<SettingsState>(context, listen: false);
    final lang = settings.appLanguage;
    
    try {
      final aiResponse = await AiService.generateRecipe(
        apiKey: settings.geminiApiKey,
        provider: settings.aiProvider,
        prompt: prompt,
        audioBase64: audioBase64,
        currentRecipe: _currentDraft,
        lang: settings.appLanguage,
      );

      if (aiResponse != null) {
        setState(() {
          _currentDraft = aiResponse.recipe;
          String extra = _currentDraft!.extraIngredients.isEmpty ? "-" : AppStrings.str(lang, _currentDraft!.extraIngredients);
          String previewText = "${aiResponse.chatMessage}\n\n📋 Preview:\n" +
              "• ${AppStrings.str(lang, 'ai_coffee')}: ${_currentDraft!.coffeeGrams}g\n" +
              "• ${AppStrings.str(lang, 'ai_water')}: ${_currentDraft!.totalWaterMl}ml\n" +
              "• ${AppStrings.str(lang, 'ai_time')}: ${_currentDraft!.totalDurationSeconds}s\n" +
              "• ${AppStrings.str(lang, 'brew_grind')}: ${_currentDraft!.targetGrindSizeMicrons} µm\n" +
              "• ${AppStrings.str(lang, 'brew_extra')}: $extra\n" +
              "• ${AppStrings.str(lang, 'phases_title')}: ${_currentDraft!.phases.length}";

          _messages.add({
            'role': 'ai',
            'text': previewText,
            'isDraft': true,
          });
        });
      } else {
        setState(() {
          _messages.add({'role': 'ai', 'text': AppStrings.str(lang, 'ai_error_general')});
        });
      }
    } catch (e) {
      setState(() {
        _messages.add({'role': 'ai', 'text': "Error: $e"});
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(AppStrings.str(Provider.of<SettingsState>(context).appLanguage, 'ai_chat_title')),
        backgroundColor: Colors.purple.shade50,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                final isUser = msg['role'] == 'user';
                final isDraft = msg['isDraft'] == true;
                
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isUser ? Colors.blue.shade100 : Colors.purple.shade50,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(msg['text']),
                        if (isDraft) ...[
                          const SizedBox(height: 8),
                          ElevatedButton(
                            onPressed: () {
                              Navigator.pop(context, _currentDraft);
                            },
                            child: Text(AppStrings.str(Provider.of<SettingsState>(context, listen: false).appLanguage, 'ai_apply_btn')),
                          )
                        ]
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: CircularProgressIndicator(),
            ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(color: Colors.grey.shade300, blurRadius: 4, offset: const Offset(0, -2))
              ]
            ),
            child: Row(
              children: [
                Expanded(
                  child: NativeTextField(
                    label: AppStrings.str(Provider.of<SettingsState>(context).appLanguage, 'ai_hint'),
                    value: '',
                    isNumber: false,
                    onChanged: (val) => _textController.text = val,
                    onDone: _sendText,
                  ),
                ),
                  IconButton(
                    tooltip: AppStrings.str(Provider.of<SettingsState>(context, listen: false).appLanguage, 'ai_send_label'),
                    icon: const Icon(Icons.send, color: Colors.blue),
                    onPressed: _sendText,
                  ),
                  IconButton(
                    tooltip: _isRecording ? AppStrings.str(Provider.of<SettingsState>(context, listen: false).appLanguage, 'ai_record_stop_label') : AppStrings.str(Provider.of<SettingsState>(context, listen: false).appLanguage, 'ai_record_start_label'),
                    icon: Icon(_isRecording ? Icons.stop : Icons.mic, color: Colors.white),
                    onPressed: () {
                       if (_isRecording) {
                         _stopRecording();
                       } else {
                         _startRecording();
                       }
                    },
                    style: IconButton.styleFrom(
                      backgroundColor: _isRecording ? Colors.red : Colors.purple,
                      padding: const EdgeInsets.all(12),
                    ),
                  ),
              ],
            ),
          )
        ],
      ),
    );
  }
}
