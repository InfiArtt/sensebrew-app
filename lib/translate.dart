import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final apiKey = 'AIzaSyAfhSwpVzfD4DPQBGn2CkouqMCgLNhg7sI';
  final url = Uri.parse('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=' + apiKey);

  final file = File('keys.json');
  final jsonStr = await file.readAsString();
  final data = jsonDecode(jsonStr);

  String prompt = "Translate the following JSON object's values from Indonesian to English. Keep the exact same keys. Return ONLY the JSON object, nothing else. Do not use Markdown formatting.\n\n" + jsonEncode(data);
  
  print('Translating...');
  try {
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        "contents": [{"parts": [{"text": prompt}]}]
      })
    );
    
    final resData = jsonDecode(response.body);
    String resText = resData['candidates'][0]['content']['parts'][0]['text'].trim();
    
    if (resText.startsWith('\\\json')) {
       resText = resText.substring(7);
       resText = resText.substring(0, resText.length - 3);
    }
    await File('translated.json').writeAsString(resText);
    print('Done!');
  } catch(e) {
    print('Error: ' + e.toString());
  }
}
