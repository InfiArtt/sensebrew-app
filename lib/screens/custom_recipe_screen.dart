import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../core/recipe.dart';
import '../core/settings_state.dart';
import '../core/app_strings.dart';
import 'ai_chat_screen.dart';
import '../widgets/native_text_field.dart';


class CustomRecipeScreen extends StatefulWidget {
  final Recipe? initialRecipe;
  const CustomRecipeScreen({super.key, this.initialRecipe});

  @override
  State<CustomRecipeScreen> createState() => _CustomRecipeScreenState();
}

class _CustomRecipeScreenState extends State<CustomRecipeScreen> {
  final _nameController = TextEditingController();
  final _noteController = TextEditingController();
  final _coffeeController = TextEditingController();
  final _waterController = TextEditingController();
  final _timeController = TextEditingController();
  final _extraIngredientsController = TextEditingController();
  int _targetGrindSizeMicrons = 800;
  String _beanType = 'Arabica';

  final List<Map<String, dynamic>> _mutablePhases = [];
  String? _hiddenAiName;
  String? _hiddenAiDesc;
  String? _hiddenAiExtra;

  @override
  void initState() {
    super.initState();
  }

  String _getActionString(String lang, PhaseAction action) {
    switch (action) {
      case PhaseAction.pourCircle: return AppStrings.str(lang, 'action_pour_circle');
      case PhaseAction.pourCenter: return AppStrings.str(lang, 'action_pour_center');
      case PhaseAction.stir: return AppStrings.str(lang, 'action_stir');
        case PhaseAction.swirl: return AppStrings.str(lang, 'action_swirl');
        case PhaseAction.cap: return AppStrings.str(lang, 'action_cap');
        case PhaseAction.flip: return AppStrings.str(lang, 'action_flip');
      case PhaseAction.wait: return AppStrings.str(lang, 'action_wait');
      case PhaseAction.press: return AppStrings.str(lang, 'action_press');
      case PhaseAction.openValve: return AppStrings.str(lang, 'action_openValve');
      case PhaseAction.closeValve: return AppStrings.str(lang, 'action_closeValve');
    }
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (widget.initialRecipe != null && _nameController.text.isEmpty) {
      final lang = Provider.of<SettingsState>(context, listen: false).appLanguage;
      final r = widget.initialRecipe!;
      _hiddenAiName = r.name;
      _hiddenAiDesc = r.description;
      _hiddenAiExtra = r.extraIngredients;
      _nameController.text = AppStrings.str(lang, r.name);
      _noteController.text = AppStrings.str(lang, r.description);
      _extraIngredientsController.text = AppStrings.str(lang, r.extraIngredients);
      
      // Snap to closest valid dropdown value to prevent crash
      final allowedGrindSizes = [400, 600, 800, 1000, 1200, 1400];
      _targetGrindSizeMicrons = allowedGrindSizes.reduce((a, b) => 
        (a - r.targetGrindSizeMicrons).abs() < (b - r.targetGrindSizeMicrons).abs() ? a : b);
      
      _beanType = r.beanType;

      _coffeeController.text = r.coffeeGrams == r.coffeeGrams.toInt() ? r.coffeeGrams.toInt().toString() : r.coffeeGrams.toString();
      _waterController.text = r.totalWaterMl == r.totalWaterMl.toInt() ? r.totalWaterMl.toInt().toString() : r.totalWaterMl.toString();
      _timeController.text = r.totalDurationSeconds.toString();

      for (var p in r.phases) {
        _mutablePhases.add({'start': p.startTimeSeconds, 'amount': p.pourAmountMl, 'action': p.action});
      }
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    _noteController.dispose();
    _extraIngredientsController.dispose();
    _coffeeController.dispose();
    _waterController.dispose();
    _timeController.dispose();
    super.dispose();
  }

  void _addPhase() {
    setState(() {
      final lastStart = _mutablePhases.isNotEmpty ? _mutablePhases.last['start'] : 0;
      _mutablePhases.add({'start': lastStart + 30, 'amount': 50.0, 'action': PhaseAction.pourCircle});
    });
  }

  void _openAiChat() async {
    // Collect current draft if any
    Recipe? currentDraft;
    if (_nameController.text.isNotEmpty || _mutablePhases.isNotEmpty) {
      final coffee = double.tryParse(_coffeeController.text) ?? 15.0;
      final water = double.tryParse(_waterController.text) ?? 250.0;
      final time = int.tryParse(_timeController.text) ?? 150;
      final phases = _mutablePhases.map((mp) {
        PhaseAction action = mp['action'] ?? PhaseAction.pourCircle;
          return RecipePhase(
            startTimeSeconds: mp['start'],
            pourAmountMl: (action == PhaseAction.pourCircle || action == PhaseAction.pourCenter) ? mp['amount'] : 0.0,
            action: action,
          );
      }).toList();
      currentDraft = Recipe(
        id: widget.initialRecipe?.id,
        name: _hiddenAiName ?? _nameController.text,
        description: _hiddenAiDesc ?? _noteController.text,
        coffeeGrams: coffee,
        totalWaterMl: water,
        totalDurationSeconds: time,
        phases: phases,
        targetGrindSizeMicrons: _targetGrindSizeMicrons,
        beanType: _beanType,
        extraIngredients: _hiddenAiExtra ?? _extraIngredientsController.text,
        method: widget.initialRecipe?.method ?? BrewMethod.v60,
      );
    }

    final newRecipe = await Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => AiChatScreen(initialRecipe: currentDraft ?? widget.initialRecipe)),
    );

    if (newRecipe != null && newRecipe is Recipe) {
        final lang = Provider.of<SettingsState>(context, listen: false).appLanguage;
        setState(() {
          _hiddenAiName = newRecipe.name;
          _hiddenAiDesc = newRecipe.description;
          _hiddenAiExtra = newRecipe.extraIngredients;
          
          _nameController.text = AppStrings.str(lang, newRecipe.name);
          _noteController.text = AppStrings.str(lang, newRecipe.description);
          _extraIngredientsController.text = AppStrings.str(lang, newRecipe.extraIngredients);
          _coffeeController.text = newRecipe.coffeeGrams == newRecipe.coffeeGrams.toInt() ? newRecipe.coffeeGrams.toInt().toString() : newRecipe.coffeeGrams.toString();
          _waterController.text = newRecipe.totalWaterMl == newRecipe.totalWaterMl.toInt() ? newRecipe.totalWaterMl.toInt().toString() : newRecipe.totalWaterMl.toString();
          _timeController.text = newRecipe.totalDurationSeconds.toString();
        
        _mutablePhases.clear();
        for (var p in newRecipe.phases) {
          _mutablePhases.add({'start': p.startTimeSeconds, 'amount': p.pourAmountMl, 'action': p.action});
        }
        _targetGrindSizeMicrons = newRecipe.targetGrindSizeMicrons;
        _beanType = newRecipe.beanType;
      });
    }
  }

  void _saveRecipe(bool saveAsNew) {
    final lang = Provider.of<SettingsState>(context, listen: false).appLanguage;
    String name = _nameController.text.isEmpty ? "Custom" : _nameController.text;
    if (_hiddenAiName != null && AppStrings.str(lang, _hiddenAiName!) == name) {
      name = _hiddenAiName!;
    }
    String note = _noteController.text;
    if (_hiddenAiDesc != null && AppStrings.str(lang, _hiddenAiDesc!) == note) {
      note = _hiddenAiDesc!;
    }
    String extra = _extraIngredientsController.text;
    if (_hiddenAiExtra != null && AppStrings.str(lang, _hiddenAiExtra!) == extra) {
      extra = _hiddenAiExtra!;
    }
    
    final coffee = double.tryParse(_coffeeController.text) ?? 15.0;
    final water = double.tryParse(_waterController.text) ?? 250.0;
    final time = int.tryParse(_timeController.text) ?? 150;

    final phases = _mutablePhases.map((mp) {
      PhaseAction action = mp['action'] ?? PhaseAction.pourCircle;
      return RecipePhase(
        startTimeSeconds: mp['start'],
        pourAmountMl: (action == PhaseAction.pourCircle || action == PhaseAction.pourCenter) ? mp['amount'] : 0.0,
        action: action,
      );
    }).toList();

    final recipe = Recipe(
      id: saveAsNew ? null : widget.initialRecipe?.id,
      name: name,
      description: note,
      coffeeGrams: coffee,
      totalWaterMl: water,
      totalDurationSeconds: time,
      phases: phases,
      targetGrindSizeMicrons: _targetGrindSizeMicrons,
      beanType: _beanType,
      extraIngredients: extra,
      method: widget.initialRecipe?.method ?? BrewMethod.v60,
    );

    Navigator.pop(context, recipe); // Return recipe to MethodRecipeScreen
  }

  @override
  Widget build(BuildContext context) {
    final settings = Provider.of<SettingsState>(context);
    final lang = settings.appLanguage;

    return Scaffold(
      appBar: AppBar(title: Text(AppStrings.str(lang, 'custom_title'))),
      body: SingleChildScrollView(padding: const EdgeInsets.all(16.0), child: Column(children: [
          // --- AI CHAT BUTTON SECTION ---
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.purple.shade50,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.purple.shade200),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                ExcludeSemantics(
                  child: Row(
                    children: [
                      const Icon(Icons.auto_awesome, color: Colors.purple),
                      const SizedBox(width: 8),
                      Text(
                        AppStrings.str(lang, 'ai_title'),
                        style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.purple),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
                ElevatedButton.icon(
                  icon: const Icon(Icons.chat_bubble_outline),
                  label: Text(AppStrings.str(lang, 'ai_chat_title'), style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    backgroundColor: Colors.purple,
                    foregroundColor: Colors.white,
                  ),
                  onPressed: _openAiChat,
                ),
              ],
            ),
          ),
          
          const SizedBox(height: 32),
          const Divider(),
          const SizedBox(height: 16),
          
          // --- MANUAL FORM SECTION ---
          ExcludeSemantics(child: Text(AppStrings.str(lang, 'recipe_name'), style: const TextStyle(fontWeight: FontWeight.bold))),
          const SizedBox(height: 8),
          NativeTextField(
            label: AppStrings.str(lang, 'recipe_name'),
            value: _nameController.text,
            isNumber: false,
            onChanged: (val) { _nameController.text = val; setState(() {}); },
          ),
          const SizedBox(height: 16),
          
          ExcludeSemantics(child: Text(AppStrings.str(lang, 'custom_recipe_desc'), style: const TextStyle(fontWeight: FontWeight.bold))),
          const SizedBox(height: 8),
          NativeTextField(
            label: AppStrings.str(lang, 'custom_recipe_desc'),
            value: _noteController.text,
            isNumber: false,
            onChanged: (val) { _noteController.text = val; setState(() {}); },
          ),

          const SizedBox(height: 16),
            ExcludeSemantics(child: Text(AppStrings.str(lang, 'brew_bean'), style: const TextStyle(fontWeight: FontWeight.bold))),
            const SizedBox(height: 8),
            Semantics(
              label: AppStrings.str(lang, 'brew_bean'),
              child: DropdownButtonFormField<String>(
                value: _beanType,
                decoration: const InputDecoration(border: OutlineInputBorder()),
                items: [
                  const DropdownMenuItem(value: 'Arabica', child: Text('Arabica')),
                  const DropdownMenuItem(value: 'Robusta', child: Text('Robusta')),
                  DropdownMenuItem(value: 'Blend', child: Text(AppStrings.str(lang, 'custom_bean_blend'))),
                  DropdownMenuItem(value: 'Liberica', child: Text('Liberica')),
                  DropdownMenuItem(value: 'Excelsa', child: Text('Excelsa')),
                  DropdownMenuItem(value: 'Bebas', child: Text(AppStrings.str(lang, 'custom_bean_bebas'))),
                ],
                onChanged: (val) {
                  if (val != null) setState(() => _beanType = val);
                },
              ),
            ),
            const SizedBox(height: 16),
            ExcludeSemantics(child: Text(AppStrings.str(lang, 'brew_grind'), style: const TextStyle(fontWeight: FontWeight.bold))),
            const SizedBox(height: 8),
            Semantics(
              label: AppStrings.str(lang, 'brew_grind'),
              child: DropdownButtonFormField<int>(
                value: _targetGrindSizeMicrons,
                decoration: const InputDecoration(border: OutlineInputBorder()),
                items: [
                  DropdownMenuItem(value: 400, child: Text(AppStrings.str(lang, 'custom_grind_400'))),
                  DropdownMenuItem(value: 600, child: Text(AppStrings.str(lang, 'custom_grind_600'))),
                  DropdownMenuItem(value: 800, child: Text(AppStrings.str(lang, 'custom_grind_800'))),
                  DropdownMenuItem(value: 1000, child: Text(AppStrings.str(lang, 'custom_grind_1000'))),
                  DropdownMenuItem(value: 1200, child: Text(AppStrings.str(lang, 'custom_grind_1200'))),
                  DropdownMenuItem(value: 1400, child: Text(AppStrings.str(lang, 'custom_grind_1400'))),
                ],
                onChanged: (val) {
                  if (val != null) setState(() { _targetGrindSizeMicrons = val; });
                },
              ),
            ),
            const SizedBox(height: 16),
            NativeTextField(
              label: AppStrings.str(lang, 'brew_extra'),
              value: _extraIngredientsController.text,
              isNumber: false,
              onChanged: (val) { _extraIngredientsController.text = val; setState(() {}); },
            ),
            const SizedBox(height: 16),

          
          ExcludeSemantics(child: Text(AppStrings.str(lang, 'coffee_grams'), style: const TextStyle(fontWeight: FontWeight.bold))),
          const SizedBox(height: 8),
          NativeTextField(
            label: AppStrings.str(lang, 'coffee_grams'),
            value: _coffeeController.text,
            isNumber: true,
            onChanged: (val) { _coffeeController.text = val; setState(() {}); },
          ),
          const SizedBox(height: 16),

          ExcludeSemantics(child: Text(AppStrings.str(lang, 'total_water'), style: const TextStyle(fontWeight: FontWeight.bold))),
          const SizedBox(height: 8),
          NativeTextField(
            label: AppStrings.str(lang, 'total_water'),
            value: _waterController.text,
            isNumber: true,
            onChanged: (val) { _waterController.text = val; setState(() {}); },
          ),
          const SizedBox(height: 16),
          
          ExcludeSemantics(child: Text(AppStrings.str(lang, 'total_time'), style: const TextStyle(fontWeight: FontWeight.bold))),
          const SizedBox(height: 8),
          NativeTextField(
            label: AppStrings.str(lang, 'total_time'),
            value: _timeController.text,
            isNumber: true,
            onChanged: (val) { _timeController.text = val; setState(() {}); },
          ),

          const SizedBox(height: 24),
          Text(AppStrings.str(lang, 'phases_title'), style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ..._mutablePhases.asMap().entries.map((entry) {
            final index = entry.key;
            final phase = entry.value;
            return Card(
              semanticContainer: false,
              margin: const EdgeInsets.symmetric(vertical: 8),
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    ExcludeSemantics(child: Text(AppStrings.str(lang, 'start_sec'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12))),
                    const SizedBox(height: 4),
                    NativeTextField(
                      label: AppStrings.str(lang, 'start_sec'),
                      value: phase['start'].toString(),
                      isNumber: true,
                      onChanged: (val) => phase['start'] = int.tryParse(val) ?? 0,
                    ),
                    const SizedBox(height: 12),
                    
                    // ACTION SELECTOR
                    ListTile(
                      contentPadding: EdgeInsets.zero,
                      title: Text(_getActionString(lang, phase['action'] ?? PhaseAction.pourCircle), style: const TextStyle(fontWeight: FontWeight.bold)),
                      trailing: const Icon(Icons.arrow_drop_down),
                      onTap: () {
                        showModalBottomSheet(
                          context: context,
                          builder: (ctx) {
                            return SafeArea(
                              child: SingleChildScrollView(
                                child: Column(
                                  mainAxisSize: MainAxisSize.min,
                                  children: PhaseAction.values.map((action) {
                                    return ListTile(
                                      title: Text(_getActionString(lang, action)),
                                      onTap: () {
                                        setState(() {
                                          phase['action'] = action;
                                        });
                                        Navigator.pop(ctx);
                                      },
                                    );
                                  }).toList(),
                                ),
                              ),
                            );
                          }
                        );
                      },
                    ),
                    const SizedBox(height: 8),

                    if ((phase['action'] ?? PhaseAction.pourCircle) == PhaseAction.pourCircle || (phase['action'] ?? PhaseAction.pourCircle) == PhaseAction.pourCenter) ...[
                      ExcludeSemantics(child: Text(AppStrings.str(lang, 'water_ml'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12))),
                      const SizedBox(height: 4),
                      NativeTextField(
                        label: AppStrings.str(lang, 'water_ml'),
                        value: (phase['amount'] as double) == (phase['amount'] as double).toInt()
                            ? (phase['amount'] as double).toInt().toString()
                            : phase['amount'].toString(),
                        isNumber: true,
                        onChanged: (val) => phase['amount'] = double.tryParse(val) ?? 0.0,
                      ),
                    ],

                    const SizedBox(height: 8),
                    Align(
                      alignment: Alignment.centerRight,
                      child: IconButton(
                        icon: const Icon(Icons.delete, color: Colors.red),
                        onPressed: () {
                          setState(() {
                            _mutablePhases.removeAt(index);
                          });
                        },
                        tooltip: AppStrings.str(lang, 'delete_phase'),
                      ),
                    ),
                  ],
                ),
              ),
            );
          }),
          ElevatedButton(
            onPressed: _addPhase,
            child: Text(AppStrings.str(lang, 'add_phase')),
          ),
          const SizedBox(height: 32),
          if (widget.initialRecipe != null) ...[
            ElevatedButton(
              onPressed: () => _saveRecipe(false),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.brown),
              child: Text(AppStrings.str(lang, 'save_overwrite'), style: const TextStyle(color: Colors.white, fontSize: 18)),
            ),
            const SizedBox(height: 8),
            OutlinedButton(
              onPressed: () => _saveRecipe(true),
              style: OutlinedButton.styleFrom(foregroundColor: Colors.brown),
              child: Text(AppStrings.str(lang, 'save_as_new'), style: const TextStyle(fontSize: 18)),
            ),
          ] else ...[
            ElevatedButton(
              onPressed: () => _saveRecipe(true),
              style: ElevatedButton.styleFrom(backgroundColor: Colors.brown),
              child: Text(AppStrings.str(lang, 'save_recipe'), style: const TextStyle(color: Colors.white, fontSize: 18)),
            ),
          ],
          const SizedBox(height: 32),
        ],
      )),
    );
  }
}






