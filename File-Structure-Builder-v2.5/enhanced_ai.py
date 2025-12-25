import re
import json
from typing import Dict, List, Tuple
from datetime import datetime

class EnhancedAI:
    def __init__(self):
        self.chat_history = []
        self.templates = {
            'web_frontend': {
                'keywords': ['react', 'vue', 'angular', 'html', 'css', 'javascript', 'frontend', 'ui', 'website', 'nextjs', 'nuxt', 'svelte', 'tailwind', 'bootstrap', 'responsive', 'spa'],
                'structure': """
src/
├── components/
│   ├── common/
│   ├── layout/
│   └── ui/
├── pages/
├── hooks/
├── services/
├── utils/
├── styles/
│   ├── globals.css
│   └── components.css
├── assets/
│   ├── images/
│   └── icons/
└── App.js
public/
├── index.html
└── favicon.ico
package.json
.gitignore
README.md
""",
                'tips': ['Use component-based architecture', 'Implement responsive design', 'Optimize for performance']
            },
            'web_backend': {
                'keywords': ['api', 'server', 'backend', 'express', 'flask', 'django', 'fastapi', 'node', 'rest', 'graphql', 'microservice', 'endpoint', 'database', 'auth'],
                'structure': """
src/
├── controllers/
├── models/
├── routes/
├── middleware/
├── services/
├── config/
│   ├── database.js
│   └── settings.js
├── utils/
└── validators/
tests/
├── unit/
└── integration/
config/
├── .env.example
└── database.json
package.json
.gitignore
README.md
""",
                'tips': ['Implement proper error handling', 'Use environment variables', 'Add input validation']
            },
            'fullstack': {
                'keywords': ['fullstack', 'full stack', 'mern', 'mean', 'full-stack', 'webapp', 'web application'],
                'structure': """
client/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── utils/
├── public/
└── package.json
server/
├── src/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   └── middleware/
├── config/
└── package.json
database/
├── migrations/
└── seeds/
docker-compose.yml
README.md
""",
                'tips': ['Separate client and server', 'Use Docker for deployment', 'Implement proper API design']
            },
            'mobile_app': {
                'keywords': ['mobile', 'app', 'android', 'ios', 'flutter', 'react native', 'kotlin', 'swift', 'xamarin'],
                'structure': """
src/
├── screens/
├── components/
├── navigation/
├── services/
│   ├── api/
│   └── storage/
├── utils/
├── hooks/
├── constants/
└── assets/
    ├── images/
    ├── fonts/
    └── icons/
android/
ios/
package.json
app.json
README.md
""",
                'tips': ['Design for multiple screen sizes', 'Optimize for performance', 'Handle offline scenarios']
            },
            'python_project': {
                'keywords': ['python', 'ml', 'data', 'analysis', 'script', 'automation', 'pandas', 'numpy', 'sklearn', 'tensorflow', 'pytorch', 'django', 'flask'],
                'structure': """
src/
├── main.py
├── models/
├── utils/
│   ├── helpers.py
│   └── logger.py
├── data/
│   ├── raw/
│   └── processed/
└── config/
    └── settings.py
tests/
├── test_main.py
└── test_utils.py
notebooks/
requirements.txt
setup.py
.gitignore
README.md
""",
                'tips': ['Use virtual environments', 'Follow PEP 8 standards', 'Add comprehensive tests']
            },
            'machine_learning': {
                'keywords': ['machine learning', 'deep learning', 'neural', 'model training', 'dataset', 'ai model', 'classification', 'regression'],
                'structure': """
data/
├── raw/
├── processed/
└── external/
notebooks/
├── exploratory/
└── experiments/
src/
├── data/
│   ├── preprocessing.py
│   └── loader.py
├── models/
│   ├── train.py
│   └── evaluate.py
├── features/
└── utils/
models/
├── saved/
└── checkpoints/
tests/
requirements.txt
README.md
""",
                'tips': ['Version your data', 'Track experiments', 'Validate model performance']
            },
            'ecommerce': {
                'keywords': ['ecommerce', 'e-commerce', 'shop', 'store', 'cart', 'payment', 'product', 'checkout', 'inventory'],
                'structure': """
src/
├── components/
│   ├── products/
│   ├── cart/
│   ├── checkout/
│   └── user/
├── pages/
│   ├── home/
│   ├── products/
│   └── orders/
├── services/
│   ├── api/
│   └── payment/
├── store/
│   ├── actions/
│   └── reducers/
└── utils/
public/
package.json
README.md
""",
                'tips': ['Implement secure payments', 'Add inventory management', 'Optimize for SEO']
            },
            'desktop_app': {
                'keywords': ['desktop', 'electron', 'tkinter', 'pyqt', 'gui', 'desktop application', 'windows', 'mac', 'linux'],
                'structure': """
src/
├── main/
├── renderer/
│   ├── components/
│   └── pages/
├── utils/
└── assets/
    ├── icons/
    └── images/
config/
build/
package.json
README.md
""",
                'tips': ['Design for cross-platform', 'Optimize bundle size', 'Handle system integration']
            }
        }
        
        self.context_keywords = {
            'database': ['mysql', 'postgresql', 'mongodb', 'sqlite', 'redis'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes'],
            'testing': ['jest', 'pytest', 'unittest', 'cypress', 'selenium'],
            'styling': ['css', 'scss', 'styled-components', 'tailwind', 'bootstrap']
        }

    def analyze_prompt(self, description: str) -> Dict:
        """Enhanced prompt analysis with context understanding"""
        description_lower = description.lower()
        words = re.findall(r'\w+', description_lower)
        
        scores = {}
        matched_keywords = {}
        context_matches = {}
        
        # Analyze project types
        for project_type, data in self.templates.items():
            score = 0
            matches = []
            
            for keyword in data['keywords']:
                if keyword in description_lower:
                    score += 3 if len(keyword) > 5 else 2
                    matches.append(keyword)
                elif any(keyword in word or word in keyword for word in words):
                    score += 1
                    matches.append(keyword)
            
            scores[project_type] = score
            matched_keywords[project_type] = matches
        
        # Analyze context
        for context, keywords in self.context_keywords.items():
            context_matches[context] = [kw for kw in keywords if kw in description_lower]
        
        best_type = max(scores, key=scores.get) if max(scores.values()) > 0 else 'general'
        confidence = 'High' if scores[best_type] >= 4 else 'Medium' if scores[best_type] >= 2 else 'Low'
        
        return {
            'type': best_type,
            'confidence': confidence,
            'score': scores[best_type],
            'matched_keywords': matched_keywords.get(best_type, []),
            'context': context_matches,
            'suggestions': self.get_suggestions_for_type(best_type, context_matches)
        }

    def get_suggestions_for_type(self, project_type: str, context: Dict) -> List[str]:
        """Get contextual suggestions"""
        suggestions = []
        
        if project_type in self.templates:
            suggestions.extend(self.templates[project_type]['tips'])
        
        if context.get('database'):
            suggestions.append(f"Consider using {context['database'][0]} for data storage")
        
        if context.get('cloud'):
            suggestions.append(f"Deploy on {context['cloud'][0]} for scalability")
            
        return suggestions[:3]

    def generate_structure(self, description: str) -> str:
        analysis = self.analyze_prompt(description)
        project_type = analysis['type']
        
        if project_type in self.templates:
            structure = self.templates[project_type]['structure'].strip()
            
            # Add context-specific folders
            if analysis['context'].get('database'):
                structure += "\ndatabase/\n├── migrations/\n└── schemas/"
            
            if analysis['context'].get('testing'):
                if 'tests/' not in structure:
                    structure += "\ntests/\n├── unit/\n└── integration/"
            
            return structure
        
        return """
src/
├── main/
├── utils/
├── config/
└── assets/
tests/
docs/
README.md
LICENSE
.gitignore
"""

    def chat_response(self, message: str) -> Dict:
        """Generate chat response with suggestions"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Add to chat history
        self.chat_history.append({
            'type': 'user',
            'message': message,
            'timestamp': timestamp
        })
        
        analysis = self.analyze_prompt(message)
        
        # Generate response
        if analysis['type'] != 'general':
            project_name = analysis['type'].replace('_', ' ').title()
            response = f"I detected a {project_name} project! "
            
            if analysis['matched_keywords']:
                response += f"Keywords found: {', '.join(analysis['matched_keywords'][:3])}. "
            
            response += f"Confidence: {analysis['confidence']}."
            
            if analysis['suggestions']:
                response += f"\n\n💡 Tips:\n• " + "\n• ".join(analysis['suggestions'])
        else:
            response = "I'll create a general project structure for you. Try being more specific about your project type for better results!"
        
        # Add AI response to history
        self.chat_history.append({
            'type': 'ai',
            'message': response,
            'timestamp': timestamp,
            'analysis': analysis
        })
        
        return {
            'response': response,
            'analysis': analysis,
            'structure': self.generate_structure(message)
        }

    def get_chat_history(self) -> List[Dict]:
        return self.chat_history[-10:]  # Last 10 messages

    def clear_chat(self):
        self.chat_history.clear()