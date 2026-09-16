enum BrewMethod {
  v60,
  frenchPress,
  aeropress,
  vietnamDrip,
  cupping,
  coldBrew,
}

enum PhaseAction {
  pourCircle, // Pour with metronome per rotation
  pourCenter, // Pour with metronome per second
  wait,       // Just wait, no metronome
  stir,       // Stir instruction
  swirl,      // Swirl instruction
  cap,        // Attach cap/plunger
  flip,       // Flip Aeropress
  press,      // Press/plunge instruction
  openValve,  // Open switch/valve
  closeValve, // Close switch/valve
  }

class RecipePhase {
  final int startTimeSeconds;
  final double pourAmountMl;
  final String instructionText;
  final PhaseAction action;

  RecipePhase({
    required this.startTimeSeconds,
    this.pourAmountMl = 0.0,
    this.instructionText = "",
    this.action = PhaseAction.pourCircle,
  });

  Map<String, dynamic> toJson() => {
    'startTimeSeconds': startTimeSeconds,
    'pourAmountMl': pourAmountMl,
    'instructionText': instructionText,
    'action': action.name,
  };

  factory RecipePhase.fromJson(Map<String, dynamic> json) => RecipePhase(
    startTimeSeconds: json['startTimeSeconds'] ?? 0,
    pourAmountMl: (json['pourAmountMl'] ?? 0.0).toDouble(),
    instructionText: json['instructionText'] ?? "",
    action: PhaseAction.values.firstWhere((e) => e.name == json['action'], orElse: () => PhaseAction.pourCircle),
  );

  RecipePhase copyWith({
    int? startTimeSeconds,
    double? pourAmountMl,
    String? instructionText,
    PhaseAction? action,
  }) {
    return RecipePhase(
      startTimeSeconds: startTimeSeconds ?? this.startTimeSeconds,
      pourAmountMl: pourAmountMl ?? this.pourAmountMl,
      instructionText: instructionText ?? this.instructionText,
      action: action ?? this.action,
    );
  }
}

class Recipe {
  final String id;
  final String name;
  final String description; // Penjelasan aturan seduh
  final double coffeeGrams;
  final double totalWaterMl;
  final List<RecipePhase> phases;
  final int totalDurationSeconds;
  final BrewMethod method;
  final String extraIngredients;
  final int targetGrindSizeMicrons;
  final String beanType;
  bool isFavorite;
  final bool isBuiltIn;

  Recipe({
    String? id,
    required this.name,
    this.description = "",
    required this.coffeeGrams,
    required this.totalWaterMl,
    required this.phases,
    required this.totalDurationSeconds,
    this.method = BrewMethod.v60,
    this.extraIngredients = "",
    this.targetGrindSizeMicrons = 800, // Default to medium
    this.beanType = 'Arabica',
    this.isFavorite = false,
    this.isBuiltIn = false,
  }) : id = id ?? "${name.replaceAll(' ', '_')}_${DateTime.now().microsecondsSinceEpoch}";

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'description': description,
    'coffeeGrams': coffeeGrams,
    'totalWaterMl': totalWaterMl,
    'phases': phases.map((p) => p.toJson()).toList(),
    'totalDurationSeconds': totalDurationSeconds,
    'method': method.name,
    'extraIngredients': extraIngredients,
    'targetGrindSizeMicrons': targetGrindSizeMicrons,
    'beanType': beanType,
    'isFavorite': isFavorite,
    'isBuiltIn': isBuiltIn,
  };

  factory Recipe.fromJson(Map<String, dynamic> json) => Recipe(
    id: json['id'],
    name: json['name'] ?? '',
    description: json['description'] ?? '',
    coffeeGrams: (json['coffeeGrams'] ?? 0.0).toDouble(),
    totalWaterMl: (json['totalWaterMl'] ?? 0.0).toDouble(),
    phases: (json['phases'] as List<dynamic>?)?.map((item) => RecipePhase.fromJson(item)).toList() ?? [],
    totalDurationSeconds: json['totalDurationSeconds'] ?? 0,
    method: BrewMethod.values.firstWhere((e) => e.name == json['method'], orElse: () => BrewMethod.v60),
    extraIngredients: json['extraIngredients'] ?? '',
    targetGrindSizeMicrons: json['targetGrindSizeMicrons'] ?? 800,
    beanType: json['beanType'] ?? 'Arabica',
    isFavorite: json['isFavorite'] ?? false,
    isBuiltIn: json['isBuiltIn'] ?? recipeDatabase.any((r) => r.name == (json['name'] ?? '')),
  );

  Recipe copyWith({
    String? id,
    String? name,
    String? description,
    double? coffeeGrams,
    double? totalWaterMl,
    List<RecipePhase>? phases,
    int? totalDurationSeconds,
    BrewMethod? method,
    String? extraIngredients,
    int? targetGrindSizeMicrons,
    String? beanType,
    bool? isFavorite,
    bool? isBuiltIn,
  }) {
    return Recipe(
      id: id ?? this.id,
      name: name ?? this.name,
      description: description ?? this.description,
      coffeeGrams: coffeeGrams ?? this.coffeeGrams,
      totalWaterMl: totalWaterMl ?? this.totalWaterMl,
      phases: phases ?? this.phases.map((p) => p.copyWith()).toList(),
      totalDurationSeconds: totalDurationSeconds ?? this.totalDurationSeconds,
      method: method ?? this.method,
      extraIngredients: extraIngredients ?? this.extraIngredients,
      targetGrindSizeMicrons: targetGrindSizeMicrons ?? this.targetGrindSizeMicrons,
      beanType: beanType ?? this.beanType,
      isFavorite: isFavorite ?? this.isFavorite,
      isBuiltIn: isBuiltIn ?? this.isBuiltIn,
    );
  }
}

List<Recipe> recipeDatabase = [
  Recipe(
    isBuiltIn: true,
    name: "James Hoffmann Ultimate V60",
    description: "desc_key_0",
    coffeeGrams: 15,
    totalWaterMl: 250,
    totalDurationSeconds: 210,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 800,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 10, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 15, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 45, pourAmountMl: 100, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 75, pourAmountMl: 100, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 105, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 110, action: PhaseAction.wait),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Tetsu Kasuya 4-6 Method",
    description: "desc_key_1",
    coffeeGrams: 20,
    totalWaterMl: 300,
    totalDurationSeconds: 210,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 1100,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 45, pourAmountMl: 70, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 90, pourAmountMl: 60, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 135, pourAmountMl: 60, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 180, pourAmountMl: 60, action: PhaseAction.pourCircle),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Osmotic Flow",
    description: "desc_key_2",
    coffeeGrams: 20,
    totalWaterMl: 300,
    totalDurationSeconds: 180,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 750,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 30, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, pourAmountMl: 90, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 60, pourAmountMl: 60, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 90, pourAmountMl: 60, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 120, pourAmountMl: 60, action: PhaseAction.pourCenter),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "April Pour-Over",
    description: "desc_key_3",
    coffeeGrams: 13,
    totalWaterMl: 200,
    totalDurationSeconds: 150,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 900,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 30, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 5, pourAmountMl: 70, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 35, pourAmountMl: 30, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 40, pourAmountMl: 70, action: PhaseAction.pourCenter),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Scott Rao V60",
    description: "desc_key_4",
    coffeeGrams: 20,
    totalWaterMl: 300,
    totalDurationSeconds: 180,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 800,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 60, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 5, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 10, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 45, pourAmountMl: 240, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 90, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 95, action: PhaseAction.wait),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Hario Official V60",
    description: "desc_key_5",
    coffeeGrams: 12,
    totalWaterMl: 120,
    totalDurationSeconds: 120,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 700,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 30, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 30, pourAmountMl: 90, action: PhaseAction.pourCircle),
        ],
  ),
Recipe(
    isBuiltIn: true,
    name: "Hario Switch (Tetsu Kasuya)",
    description: "desc_key_6",
    coffeeGrams: 20,
    totalWaterMl: 300,
    totalDurationSeconds: 150,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 800,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 150, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 65, action: PhaseAction.closeValve),
          RecipePhase(startTimeSeconds: 75, pourAmountMl: 150, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 120, action: PhaseAction.openValve),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Clever Dripper / Full Immersion",
    description: "desc_key_7",
    coffeeGrams: 15,
    totalWaterMl: 250,
    totalDurationSeconds: 180,
    method: BrewMethod.v60,
    targetGrindSizeMicrons: 850,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 250, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 40, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 120, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 130, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 150, action: PhaseAction.openValve),
        ],
  ),

  // ====================================
  // FRENCH PRESS RECIPES (Total 10)
  // ====================================,
  Recipe(
    isBuiltIn: true,
    name: "James Hoffmann French Press",
    description: "desc_key_8",
    coffeeGrams: 30,
    totalWaterMl: 500,
    totalDurationSeconds: 570,
    method: BrewMethod.frenchPress,
    targetGrindSizeMicrons: 900,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 500, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 240, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 250, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 540, action: PhaseAction.press),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Traditional French Press",
    description: "desc_key_9",
    coffeeGrams: 30,
    totalWaterMl: 500,
    totalDurationSeconds: 270,
    method: BrewMethod.frenchPress,
    targetGrindSizeMicrons: 1100,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 500, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 60, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 70, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 240, action: PhaseAction.press),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Cafe au Lait (Strong French Press)",
    description: "desc_key_10",
    coffeeGrams: 30,
    totalWaterMl: 300,
      extraIngredients: "extra_key_0",
    totalDurationSeconds: 270,
    method: BrewMethod.frenchPress,
    targetGrindSizeMicrons: 1000,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 300, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 60, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 70, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 240, action: PhaseAction.press),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Lance Hedrick French Press",
    description: "desc_key_11",
    coffeeGrams: 30,
    totalWaterMl: 500,
    totalDurationSeconds: 330,
    method: BrewMethod.frenchPress,
    targetGrindSizeMicrons: 800,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 500, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 40, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 300, action: PhaseAction.press),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Slayer French Press (Skim Early)",
    description: "desc_key_12",
    coffeeGrams: 30,
    totalWaterMl: 500,
    totalDurationSeconds: 270,
    method: BrewMethod.frenchPress,
    targetGrindSizeMicrons: 950,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 500, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 60, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 70, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 240, action: PhaseAction.press),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "French Press Cold Water Bloom",
    description: "desc_key_13",
      coffeeGrams: 30,
      totalWaterMl: 500,
      totalDurationSeconds: 330,
      method: BrewMethod.frenchPress,
      targetGrindSizeMicrons: 1000,
      phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 60, pourAmountMl: 450, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 300, action: PhaseAction.press),
        ],
    ),
  Recipe(
    isBuiltIn: true,
    name: "Tim Wendelboe French Press",
    description: "desc_key_14",
      coffeeGrams: 30,
      totalWaterMl: 500,
      totalDurationSeconds: 570,
      method: BrewMethod.frenchPress,
      targetGrindSizeMicrons: 1000,
      phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 500, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 240, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 250, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 540, action: PhaseAction.press),
        ],
    ),

  // ====================================
  // AEROPRESS RECIPES (Total 10)
  // ====================================,
  Recipe(
    isBuiltIn: true,
    name: "Alan Adler (Original)",
      extraIngredients: "extra_key_1",
      description: "desc_key_15",
      coffeeGrams: 15,
      totalWaterMl: 60,
    totalDurationSeconds: 90,
    method: BrewMethod.aeropress,
    targetGrindSizeMicrons: 500,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 60, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 15, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 25, action: PhaseAction.press),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Tim Wendelboe Aeropress",
    description: "desc_key_16",
    coffeeGrams: 14,
    totalWaterMl: 200,
    totalDurationSeconds: 80,
    method: BrewMethod.aeropress,
    targetGrindSizeMicrons: 700,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 200, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 15, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 18, action: PhaseAction.wait),
            RecipePhase(startTimeSeconds: 20, action: PhaseAction.cap),
          RecipePhase(startTimeSeconds: 25, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "James Hoffmann Ultimate Aeropress",
    description: "desc_key_17",
    coffeeGrams: 11,
    totalWaterMl: 200,
    totalDurationSeconds: 180,
    method: BrewMethod.aeropress,
    targetGrindSizeMicrons: 650,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 200, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 15, action: PhaseAction.cap),
          RecipePhase(startTimeSeconds: 19, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 25, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 120, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 125, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 150, action: PhaseAction.press),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Inverted Classic",
    description: "desc_key_18",
    coffeeGrams: 15,
    totalWaterMl: 200,
    totalDurationSeconds: 150,
    method: BrewMethod.aeropress,
    targetGrindSizeMicrons: 700,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 200, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 33, action: PhaseAction.wait),
            RecipePhase(startTimeSeconds: 40, action: PhaseAction.cap),
          RecipePhase(startTimeSeconds: 45, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 90, action: PhaseAction.flip),
          RecipePhase(startTimeSeconds: 95, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 120, action: PhaseAction.press),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Aeropress Espresso Concentrate",
    description: "desc_key_19",
    coffeeGrams: 18,
    totalWaterMl: 90,
    totalDurationSeconds: 120,
    method: BrewMethod.aeropress,
    targetGrindSizeMicrons: 450,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 90, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 33, action: PhaseAction.wait),
            RecipePhase(startTimeSeconds: 40, action: PhaseAction.cap),
          RecipePhase(startTimeSeconds: 45, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 70, action: PhaseAction.flip),
          RecipePhase(startTimeSeconds: 75, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Aeropress Milk Punch",
    description: "desc_key_20",
    coffeeGrams: 18,
    totalWaterMl: 80,
    extraIngredients: "extra_key_2",
    totalDurationSeconds: 120,
    method: BrewMethod.aeropress,
    targetGrindSizeMicrons: 500,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 80, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 33, action: PhaseAction.wait),
            RecipePhase(startTimeSeconds: 40, action: PhaseAction.cap),
          RecipePhase(startTimeSeconds: 45, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "WAC 2023 Champion Recipe",
    description: "desc_key_21",
      coffeeGrams: 16,
      totalWaterMl: 220,
      totalDurationSeconds: 150,
      method: BrewMethod.aeropress,
      targetGrindSizeMicrons: 600,
      extraIngredients: "extra_key_3",
      phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 140, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 10, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 15, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),
          RecipePhase(startTimeSeconds: 115, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 120, pourAmountMl: 80, action: PhaseAction.pourCenter),
        ],
    ),
  Recipe(
    isBuiltIn: true,
    name: "Jonathan Gagne Long Steep",
    description: "desc_key_22",
      coffeeGrams: 20,
      totalWaterMl: 300,
      totalDurationSeconds: 570,
      method: BrewMethod.aeropress,
      targetGrindSizeMicrons: 800,
      phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 300, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 540, action: PhaseAction.press),
        ],
    ),
  Recipe(
      isBuiltIn: true,
      name: "Aeropress Iced Coffee",
      description: "desc_key_23",
      coffeeGrams: 18,
      totalWaterMl: 100,
      totalDurationSeconds: 90,
      method: BrewMethod.aeropress,
      targetGrindSizeMicrons: 400,
      extraIngredients: "extra_key_4",
      phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 100, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 10, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 14, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 20, action: PhaseAction.cap),
          RecipePhase(startTimeSeconds: 25, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),
        ],
    ),
  Recipe(
    isBuiltIn: true,
    name: "Aeropress Espresso (Faux-Presso)",
    description: "desc_key_24",
      coffeeGrams: 18,
      totalWaterMl: 50,
      totalDurationSeconds: 90,
      method: BrewMethod.aeropress,
      targetGrindSizeMicrons: 400,
      phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 10, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 14, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 20, action: PhaseAction.cap),
          RecipePhase(startTimeSeconds: 25, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),
        ],
    ),

  // ====================================
  // VIETNAM DRIP RECIPES (Total 10)
  // ====================================,
  Recipe(
    isBuiltIn: true,
    name: "Tradisional Vietnam Drip",
    description: "desc_key_25",
    coffeeGrams: 15,
      beanType: "Robusta",
    totalWaterMl: 120,
    extraIngredients: "extra_key_7",
    totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 800,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, pourAmountMl: 100, action: PhaseAction.pourCenter),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Ca Phe Sua Da (Kopi Susu Es)",
    description: "desc_key_26",
    coffeeGrams: 20,
      beanType: "Robusta",
    totalWaterMl: 100,
    extraIngredients: "extra_key_5",
    totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 750,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 40, pourAmountMl: 80, action: PhaseAction.pourCenter),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Ca Phe Den (Kopi Hitam)",
    description: "desc_key_27",
    coffeeGrams: 15,
    totalWaterMl: 150,
    totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 900,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 25, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 40, pourAmountMl: 125, action: PhaseAction.pourCenter),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Modern Specialty Drip",
    description: "desc_key_28",
    coffeeGrams: 15,
    totalWaterMl: 225,
    totalDurationSeconds: 240,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 850,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 40, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 45, pourAmountMl: 185, action: PhaseAction.pourCenter),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Drip Ristretto Style",
    description: "desc_key_29",
    coffeeGrams: 20,
    totalWaterMl: 60,
    totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 700,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 60, action: PhaseAction.pourCenter),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Vietnam Drip Gula Aren",
    description: "desc_key_30",
    coffeeGrams: 18,
      beanType: "Robusta",
    totalWaterMl: 130,
    extraIngredients: "extra_key_6",
    totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 800,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 30, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 40, pourAmountMl: 100, action: PhaseAction.pourCenter),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Vietnam Drip Paper Filter Method",
    description: "desc_key_31",
    coffeeGrams: 15,
      beanType: "Robusta",
    totalWaterMl: 120,
    totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 800,
    extraIngredients: "extra_key_7",
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, pourAmountMl: 100, action: PhaseAction.pourCenter),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Specialty High-Ratio Drip (1:12)",
    description: "desc_key_32",
    coffeeGrams: 15,
    totalWaterMl: 180,
    totalDurationSeconds: 240,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 1000,
    extraIngredients: "",
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 30, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, pourAmountMl: 150, action: PhaseAction.pourCenter),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Double Tamp Vietnam Drip",
    description: "desc_key_33",
      coffeeGrams: 20,
      beanType: "Robusta",
      totalWaterMl: 100,
      totalDurationSeconds: 360,
      method: BrewMethod.vietnamDrip,
      targetGrindSizeMicrons: 800,
      extraIngredients: "",
      phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, action: PhaseAction.press),
          RecipePhase(startTimeSeconds: 35, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 45, pourAmountMl: 80, action: PhaseAction.pourCenter),
        ],
    ),

  // ====================================
  // CUPPING RECIPES (Total 10)
  // ====================================,
  Recipe(
    isBuiltIn: true,
    name: "SCA Cupping Protocol",
    description: "desc_key_34",
    coffeeGrams: 11,
    totalWaterMl: 200,
    totalDurationSeconds: 660,
    method: BrewMethod.cupping,
      beanType: 'Bebas',
    targetGrindSizeMicrons: 850,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 200, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 240, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 245, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 600, action: PhaseAction.wait),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "James Hoffmann Home Cupping",
    description: "desc_key_35",
    coffeeGrams: 12,
    totalWaterMl: 200,
    totalDurationSeconds: 750,
    method: BrewMethod.cupping,
      beanType: 'Bebas',
    targetGrindSizeMicrons: 850,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 200, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 240, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 245, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 720, action: PhaseAction.wait),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Cold Evaluation Cupping",
    description: "desc_key_36",
    coffeeGrams: 11,
    totalWaterMl: 200,
    totalDurationSeconds: 930,
    method: BrewMethod.cupping,
      beanType: 'Bebas',
    targetGrindSizeMicrons: 850,
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 200, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 240, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 250, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 900, action: PhaseAction.wait),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Minimal Agitation Cupping",
    description: "desc_key_37",
      coffeeGrams: 12,
      totalWaterMl: 200,
      totalDurationSeconds: 750,
      method: BrewMethod.cupping,
      beanType: 'Bebas',
      targetGrindSizeMicrons: 800,
      phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 200, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 720, action: PhaseAction.wait),
        ],
    ),

  // ====================================
  // COLD BREW RECIPES (Total 10)
  // ====================================,
  Recipe(
    isBuiltIn: true,
    name: "Japanese Iced Coffee (Fruity)",
    description: "desc_key_38",
    coffeeGrams: 15, totalWaterMl: 150,
      extraIngredients: "extra_key_8", totalDurationSeconds: 150,
    method: BrewMethod.v60, targetGrindSizeMicrons: 700, beanType: 'Arabica',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 40, pourAmountMl: 100, action: PhaseAction.pourCircle),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Japanese Iced Coffee (Sweet)",
    description: "desc_key_39",
    coffeeGrams: 15, totalWaterMl: 150,
      extraIngredients: "extra_key_9", totalDurationSeconds: 180,
    method: BrewMethod.v60, targetGrindSizeMicrons: 750, beanType: 'Arabica',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 40, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 45, pourAmountMl: 55, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 90, pourAmountMl: 55, action: PhaseAction.pourCircle),
        ],
  ),


  Recipe(
    isBuiltIn: true,
    name: "Ryan Wibawa WBrC 2024",
    description: "desc_key_40",
    coffeeGrams: 16, totalWaterMl: 240, totalDurationSeconds: 160,
    method: BrewMethod.v60, targetGrindSizeMicrons: 800, beanType: 'Arabica',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 40, pourAmountMl: 70, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 80, pourAmountMl: 60, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 110, pourAmountMl: 60, action: PhaseAction.pourCircle),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Yoshua Tanu Fast Flow",
    description: "desc_key_41",
    coffeeGrams: 15, totalWaterMl: 225, totalDurationSeconds: 120,
    method: BrewMethod.v60, targetGrindSizeMicrons: 900, beanType: 'Arabica',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 45, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 5, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 10, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 30, pourAmountMl: 90, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 70, pourAmountMl: 90, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 80, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 85, action: PhaseAction.wait),
        ],
  ),
  Recipe(
    isBuiltIn: true,
    name: "Orea V3/Kalita Wave",
    description: "desc_key_42",
    coffeeGrams: 15, totalWaterMl: 250, totalDurationSeconds: 150,
    method: BrewMethod.v60, targetGrindSizeMicrons: 800, beanType: 'Arabica',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 40, pourAmountMl: 100, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 80, pourAmountMl: 100, action: PhaseAction.pourCenter),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "V60 Dark Roast (Low Temp)",
    description: "desc_key_43",
    coffeeGrams: 15, totalWaterMl: 250, totalDurationSeconds: 140,
    method: BrewMethod.v60, targetGrindSizeMicrons: 900, beanType: 'Blend',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 45, pourAmountMl: 100, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 85, pourAmountMl: 100, action: PhaseAction.pourCenter),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "Kasuya Devil Recipe (Switch)",
    description: "desc_key_44",
    coffeeGrams: 20, totalWaterMl: 280, totalDurationSeconds: 200,
    method: BrewMethod.v60, targetGrindSizeMicrons: 850, beanType: 'Arabica',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 60, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 40, action: PhaseAction.closeValve),
          RecipePhase(startTimeSeconds: 42, pourAmountMl: 120, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 80, pourAmountMl: 100, action: PhaseAction.pourCircle),
          RecipePhase(startTimeSeconds: 120, action: PhaseAction.openValve),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "W.A.C Carolina Ibarra (2018)",
    description: "desc_key_45",
    coffeeGrams: 35, totalWaterMl: 100, totalDurationSeconds: 90,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 800, beanType: 'Arabica',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 100, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 33, action: PhaseAction.wait),
            RecipePhase(startTimeSeconds: 40, action: PhaseAction.cap),
          RecipePhase(startTimeSeconds: 46, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 55, action: PhaseAction.flip),
          RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "W.A.C Paulina Miczka (2017)",
    description: "desc_key_46",
    coffeeGrams: 35, totalWaterMl: 150, totalDurationSeconds: 105,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 850, beanType: 'Arabica',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 150, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 15, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 25, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 35, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 38, action: PhaseAction.wait),
            RecipePhase(startTimeSeconds: 45, action: PhaseAction.cap),
          RecipePhase(startTimeSeconds: 51, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 70, action: PhaseAction.flip),
          RecipePhase(startTimeSeconds: 75, action: PhaseAction.press),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "Tuomas Merikanto W.A.C",
    description: "desc_key_47",
    coffeeGrams: 18, totalWaterMl: 200, totalDurationSeconds: 150,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 750, beanType: 'Arabica',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 50, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 10, action: PhaseAction.swirl),
          RecipePhase(startTimeSeconds: 15, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 45, pourAmountMl: 150, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "Aeropress Flow Control",
    description: "desc_key_48",
    coffeeGrams: 18, totalWaterMl: 250, totalDurationSeconds: 150,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 700, beanType: 'Arabica',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 250, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 40, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 120, action: PhaseAction.press),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "Aeropress Espresso Fake",
    description: "desc_key_49",
    coffeeGrams: 20, totalWaterMl: 60, totalDurationSeconds: 90,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 300, beanType: 'Blend',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 60, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 20, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 30, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 60, action: PhaseAction.press),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "Aeropress Tea-like Extract",
    description: "desc_key_50",
    coffeeGrams: 12, totalWaterMl: 250, totalDurationSeconds: 180,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 1000, beanType: 'Arabica',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 250, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 150, action: PhaseAction.press),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "Aeropress Robusta Sweet",
    description: "desc_key_51",
    coffeeGrams: 15, totalWaterMl: 60,
      extraIngredients: "extra_key_10", totalDurationSeconds: 120,
    method: BrewMethod.aeropress, targetGrindSizeMicrons: 700, beanType: 'Robusta',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 60, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, action: PhaseAction.stir),
          RecipePhase(startTimeSeconds: 40, action: PhaseAction.wait),
          RecipePhase(startTimeSeconds: 90, action: PhaseAction.press),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "Ca Phe Muoi (Salted Coffee)",
    description: "desc_key_52",
    coffeeGrams: 20,
      extraIngredients: "extra_key_11", totalWaterMl: 100, totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 650, beanType: 'Robusta',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, pourAmountMl: 80, action: PhaseAction.pourCenter),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "Ca Phe Trung (Egg Coffee)",
    description: "desc_key_53",
    coffeeGrams: 20,
      extraIngredients: "extra_key_12", totalWaterMl: 80, totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 650, beanType: 'Robusta',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 45, pourAmountMl: 60, action: PhaseAction.pourCenter),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "Ca Phe Sua Chua (Yogurt Coffee)",
    description: "desc_key_54",
    coffeeGrams: 15,
      extraIngredients: "extra_key_13", totalWaterMl: 100, totalDurationSeconds: 240,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 700, beanType: 'Robusta',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, pourAmountMl: 80, action: PhaseAction.pourCenter),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "Phin Arabica Light",
    description: "desc_key_55",
    coffeeGrams: 15, totalWaterMl: 120, totalDurationSeconds: 240,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 800, beanType: 'Arabica',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 30, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 45, pourAmountMl: 90, action: PhaseAction.pourCenter),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "Vietnam Drip Mocha",
    description: "desc_key_56",
    coffeeGrams: 15,
      extraIngredients: "extra_key_14", totalWaterMl: 100, totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip, targetGrindSizeMicrons: 700, beanType: 'Blend',
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 30, pourAmountMl: 80, action: PhaseAction.pourCenter),
        ],
  ),

  Recipe(
    isBuiltIn: true,
    name: "Phin Coconut (Bac Xiu)",
    description: "desc_key_57",
    coffeeGrams: 15,
    totalWaterMl: 60,
    totalDurationSeconds: 300,
    method: BrewMethod.vietnamDrip,
    targetGrindSizeMicrons: 700,
    beanType: 'Robusta',
    extraIngredients: "extra_key_15",
    phases: [
          RecipePhase(startTimeSeconds: 0, pourAmountMl: 20, action: PhaseAction.pourCenter),
          RecipePhase(startTimeSeconds: 45, pourAmountMl: 40, action: PhaseAction.pourCenter),
        ],
  )

];

