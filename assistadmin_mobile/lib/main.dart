import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() => runApp(AssistAdminApp());

class AssistAdminApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AssistAdmin Pro',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: LoginPage(),
    );
  }
}

class LoginPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('AssistAdmin Pro')),
      body: Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(decoration: InputDecoration(labelText: 'Nom utilisateur')),
            SizedBox(height: 10),
            TextField(decoration: InputDecoration(labelText: 'Mot de passe'), obscureText: true),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => HomePage())),
              child: Text('Connexion'),
            ),
          ],
        ),
      ),
    );
  }
}

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('AssistAdmin Pro'), automaticallyImplyLeading: false),
      body: GridView.count(
        crossAxisCount: 2,
        padding: EdgeInsets.all(16),
        children: [
          _card(context, '📄 CV', '2 000 - 5 000 FCFA', CvPage()),
          _card(context, '✉️ Lettres', '1 000 - 3 000 FCFA', LetterPage()),
          _card(context, '📁 Dossiers', 'Sur devis', DossierPage()),
          _card(context, '🔧 Correction', '1 000 - 3 000 FCFA', CorrectionPage()),
        ],
      ),
    );
  }

  Widget _card(BuildContext context, String title, String price, Widget page) {
    return Card(
      child: InkWell(
        onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => page)),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(title, style: TextStyle(fontSize: 28)),
              SizedBox(height: 8),
              Text(price, style: TextStyle(color: Colors.green, fontSize: 12)),
            ],
          ),
        ),
      ),
    );
  }
}

// ==================== PAGE CV ====================
class CvPage extends StatefulWidget {
  @override
  _CvPageState createState() => _CvPageState();
}

class _CvPageState extends State<CvPage> {
  final TextEditingController nom = TextEditingController();
  final TextEditingController email = TextEditingController();
  final TextEditingController tel = TextEditingController();
  final TextEditingController experience = TextEditingController();
  final TextEditingController formation = TextEditingController();
  final TextEditingController competences = TextEditingController();
  String result = '';

  void generate() {
    setState(() {
      result = '''Génère un CV professionnel pour :

Nom: ${nom.text}
Email: ${email.text}
Téléphone: ${tel.text}

Expériences:
${experience.text}

Formations:
${formation.text}

Compétences:
${competences.text}

Format professionnel adapté au contexte ouest-africain.''';
    });
  }

  void copy() {
    Clipboard.setData(ClipboardData(text: result));
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('✅ Prompt copié ! Allez sur claude.ai')));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('📄 CV Professionnel')),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(children: [
          TextField(controller: nom, decoration: InputDecoration(labelText: 'Nom complet')),
          TextField(controller: email, decoration: InputDecoration(labelText: 'Email')),
          TextField(controller: tel, decoration: InputDecoration(labelText: 'Téléphone')),
          TextField(controller: experience, decoration: InputDecoration(labelText: 'Expériences'), maxLines: 3),
          TextField(controller: formation, decoration: InputDecoration(labelText: 'Formations'), maxLines: 2),
          TextField(controller: competences, decoration: InputDecoration(labelText: 'Compétences (séparées par virgules)')),
          SizedBox(height: 20),
          ElevatedButton(onPressed: generate, child: Text('🎯 Générer le prompt')),
          if (result.isNotEmpty) ...[
            SizedBox(height: 20),
            Container(padding: EdgeInsets.all(12), color: Colors.grey[200], child: SelectableText(result)),
            SizedBox(height: 10),
            ElevatedButton.icon(onPressed: copy, icon: Icon(Icons.copy), label: Text('📋 Copier')),
          ],
        ]),
      ),
    );
  }
}

// ==================== PAGE LETTRES ====================
class LetterPage extends StatefulWidget {
  @override
  _LetterPageState createState() => _LetterPageState();
}

class _LetterPageState extends State<LetterPage> {
  final TextEditingController type = TextEditingController();
  final TextEditingController destinataire = TextEditingController();
  final TextEditingController objet = TextEditingController();
  final TextEditingController message = TextEditingController();
  String result = '';

  void generate() {
    setState(() {
      result = '''Rédige une ${type.text} professionnelle :

Destinataire: ${destinataire.text}
Objet: ${objet.text}

Message:
${message.text}

Style formel et professionnel, adapté au contexte administratif.''';
    });
  }

  void copy() {
    Clipboard.setData(ClipboardData(text: result));
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('✅ Prompt copié !')));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('✉️ Lettres')),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(children: [
          TextField(controller: type, decoration: InputDecoration(labelText: 'Type (motivation/administrative/réclamation)')),
          TextField(controller: destinataire, decoration: InputDecoration(labelText: 'Destinataire')),
          TextField(controller: objet, decoration: InputDecoration(labelText: 'Objet')),
          TextField(controller: message, decoration: InputDecoration(labelText: 'Message spécifique'), maxLines: 4),
          SizedBox(height: 20),
          ElevatedButton(onPressed: generate, child: Text('🎯 Générer le prompt')),
          if (result.isNotEmpty) ...[
            SizedBox(height: 20),
            Container(padding: EdgeInsets.all(12), color: Colors.grey[200], child: SelectableText(result)),
            SizedBox(height: 10),
            ElevatedButton.icon(onPressed: copy, icon: Icon(Icons.copy), label: Text('📋 Copier')),
          ],
        ]),
      ),
    );
  }
}

// ==================== PAGE DOSSIERS ====================
class DossierPage extends StatefulWidget {
  @override
  _DossierPageState createState() => _DossierPageState();
}

class _DossierPageState extends State<DossierPage> {
  final TextEditingController typeDossier = TextEditingController();
  final TextEditingController situation = TextEditingController();
  final TextEditingController ville = TextEditingController();
  String result = '';

  void generate() {
    setState(() {
      result = '''Guide pour ${typeDossier.text} :

Ville: ${ville.text}
Situation: ${situation.text}

Fournis:
1. Documents nécessaires
2. Démarches étape par étape
3. Délais et coûts
4. Astuces pratiques''';
    });
  }

  void copy() {
    Clipboard.setData(ClipboardData(text: result));
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('✅ Prompt copié !')));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('📁 Assistant Dossiers')),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(children: [
          TextField(controller: typeDossier, decoration: InputDecoration(labelText: 'Type (CNI/Passeport/Attestation)')),
          TextField(controller: ville, decoration: InputDecoration(labelText: 'Ville/Département')),
          TextField(controller: situation, decoration: InputDecoration(labelText: 'Votre situation'), maxLines: 3),
          SizedBox(height: 20),
          ElevatedButton(onPressed: generate, child: Text('🎯 Générer le guide')),
          if (result.isNotEmpty) ...[
            SizedBox(height: 20),
            Container(padding: EdgeInsets.all(12), color: Colors.grey[200], child: SelectableText(result)),
            SizedBox(height: 10),
            ElevatedButton.icon(onPressed: copy, icon: Icon(Icons.copy), label: Text('📋 Copier')),
          ],
        ]),
      ),
    );
  }
}

// ==================== PAGE CORRECTION ====================
class CorrectionPage extends StatefulWidget {
  @override
  _CorrectionPageState createState() => _CorrectionPageState();
}

class _CorrectionPageState extends State<CorrectionPage> {
  final TextEditingController typeDoc = TextEditingController();
  final TextEditingController texte = TextEditingController();
  String result = '';

  void generate() {
    setState(() {
      result = '''Corrige ce ${typeDoc.text} :

---
${texte.text}
---

1. Corrige les erreurs (orthographe, grammaire)
2. Améliore la clarté et la fluidité
3. Propose une version améliorée complète
4. Donne des conseils d'amélioration''';
    });
  }

  void copy() {
    Clipboard.setData(ClipboardData(text: result));
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('✅ Prompt copié !')));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('🔧 Correction')),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(children: [
          TextField(controller: typeDoc, decoration: InputDecoration(labelText: 'Type (CV/Lettre/Email/Rapport)')),
          TextField(controller: texte, decoration: InputDecoration(labelText: 'Texte à corriger'), maxLines: 6),
          SizedBox(height: 20),
          ElevatedButton(onPressed: generate, child: Text('🎯 Générer la correction')),
          if (result.isNotEmpty) ...[
            SizedBox(height: 20),
            Container(padding: EdgeInsets.all(12), color: Colors.grey[200], child: SelectableText(result)),
            SizedBox(height: 10),
            ElevatedButton.icon(onPressed: copy, icon: Icon(Icons.copy), label: Text('📋 Copier')),
          ],
        ]),
      ),
    );
  }
}

// ==================== PAGE PAIEMENT ====================
class PaymentPage extends StatefulWidget {
  final String service;
  final int amount;
  final String documentType;
  PaymentPage({required this.service, required this.amount, required this.documentType});

  @override
  _PaymentPageState createState() => _PaymentPageState();
}

class _PaymentPageState extends State<PaymentPage> {
  final TextEditingController phoneController = TextEditingController();
  String status = '';

  void processPayment() async {
    setState(() => status = 'Traitement en cours...');
    
    // Simulation d'appel API
    await Future.delayed(Duration(seconds: 2));
    
    setState(() {
      status = '''✅ Paiement de ${widget.amount} FCFA initié !
      
Service: ${widget.service.toUpperCase()}
Numéro: ${phoneController.text}
Document: ${widget.documentType}

📱 Vous allez recevoir une notification sur votre téléphone.
Code de vérification: ${DateTime.now().millisecondsSinceEpoch.toString().substring(10, 15)}''';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('💳 Paiement ${widget.service.toUpperCase()}')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(children: [
          Text('Montant: ${widget.amount} FCFA', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          Text('Service: ${widget.documentType}', style: TextStyle(fontSize: 16)),
          SizedBox(height: 30),
          TextField(controller: phoneController, decoration: InputDecoration(labelText: 'Numéro de téléphone'), keyboardType: TextInputType.phone),
          SizedBox(height: 20),
          ElevatedButton(onPressed: processPayment, child: Text('💰 Confirmer le paiement')),
          if (status.isNotEmpty) ...[
            SizedBox(height: 20),
            Container(padding: EdgeInsets.all(12), color: Colors.green[100], child: Text(status)),
          ],
        ]),
      ),
    );
  }
}
