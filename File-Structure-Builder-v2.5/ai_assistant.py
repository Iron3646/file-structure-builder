import re
from typing import Dict, List

class ProjectStructureAI:
    def __init__(self):
        self.project_patterns = {
            'web_frontend': {
                'keywords': ['react', 'vue', 'angular', 'html', 'css', 'javascript', 'frontend', 'ui', 'website', 'nextjs', 'nuxt', 'svelte', 'tailwind', 'bootstrap'],
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
│   └── variables.css
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
"""
            },
            'web_backend': {
                'keywords': ['api', 'server', 'backend', 'express', 'flask', 'django', 'fastapi', 'node', 'rest', 'graphql', 'microservice', 'endpoint'],
                'structure': """
src/
├── controllers/
├── models/
├── routes/
├── middleware/
├── services/
├── config/
│   ├── database.py
│   └── settings.py
├── utils/
└── validators/
tests/
├── unit/
└── integration/
requirements.txt
app.py
.env.example
.gitignore
README.md
"""
            },
            'fullstack': {
                'keywords': ['fullstack', 'full stack', 'mern', 'mean', 'full-stack', 'webapp'],
                'structure': """
client/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
├── public/
└── package.json
server/
├── src/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   └── middleware/
├── config/
└── app.js
database/
├── migrations/
└── seeds/
README.md
.gitignore
"""
            },
            'mobile_app': {
                'keywords': ['mobile', 'app', 'android', 'ios', 'flutter', 'react native', 'kotlin', 'swift'],
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
"""
            },
            'python_project': {
                'keywords': ['python', 'ml', 'data', 'analysis', 'script', 'automation', 'pandas', 'numpy', 'sklearn', 'tensorflow', 'pytorch'],
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
"""
            },
            'machine_learning': {
                'keywords': ['machine learning', 'deep learning', 'neural', 'model training', 'dataset', 'ai model'],
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
"""
            },
            'java_project': {
                'keywords': ['java', 'spring', 'maven', 'gradle', 'springboot', 'hibernate'],
                'structure': """
src/
├── main/
│   ├── java/
│   │   └── com/
│   │       └── example/
│   │           ├── controller/
│   │           ├── service/
│   │           ├── repository/
│   │           ├── model/
│   │           └── Application.java
│   └── resources/
│       ├── application.properties
│       └── static/
└── test/
    └── java/
pom.xml
.gitignore
README.md
"""
            },
            'game_project': {
                'keywords': ['game', 'unity', 'unreal', 'pygame', 'godot', 'gamedev'],
                'structure': """
Assets/
├── Scripts/
│   ├── Player/
│   ├── Enemy/
│   └── Managers/
├── Scenes/
├── Prefabs/
├── Materials/
├── Textures/
├── Audio/
│   ├── Music/
│   └── SFX/
└── Animations/
ProjectSettings/
README.md
"""
            },
            'ecommerce': {
                'keywords': ['ecommerce', 'e-commerce', 'shop', 'store', 'cart', 'payment', 'product'],
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
"""
            },
            'blog_cms': {
                'keywords': ['blog', 'cms', 'content', 'wordpress', 'article', 'post'],
                'structure': """
src/
├── components/
│   ├── posts/
│   ├── editor/
│   └── comments/
├── pages/
│   ├── admin/
│   └── public/
├── models/
│   ├── Post.js
│   └── User.js
├── services/
└── utils/
public/
├── uploads/
└── assets/
README.md
"""
            },
            'desktop_app': {
                'keywords': ['desktop', 'electron', 'tkinter', 'pyqt', 'gui', 'desktop application'],
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
"""
            }
        }

    def analyze_prompt(self, description: str) -> Dict:
        """Deep analysis of user prompt"""
        description_lower = description.lower()
        words = re.findall(r'\w+', description_lower)
        
        # Score each project type
        scores = {}
        matched_keywords = {}
        
        for project_type, data in self.project_patterns.items():
            score = 0
            matches = []
            
            for keyword in data['keywords']:
                # Exact match
                if keyword in description_lower:
                    score += 2
                    matches.append(keyword)
                # Partial match
                elif any(keyword in word or word in keyword for word in words):
                    score += 1
                    matches.append(keyword)
            
            scores[project_type] = score
            matched_keywords[project_type] = matches
        
        # Get best match
        best_type = max(scores, key=scores.get) if max(scores.values()) > 0 else 'general'
        confidence = 'High' if scores[best_type] >= 3 else 'Medium' if scores[best_type] >= 1 else 'Low'
        
        return {
            'type': best_type,
            'confidence': confidence,
            'score': scores[best_type],
            'matched_keywords': matched_keywords.get(best_type, [])
        }

    def detect_project_type(self, description: str) -> str:
        analysis = self.analyze_prompt(description)
        return analysis['type']

    def generate_structure(self, description: str) -> str:
        project_type = self.detect_project_type(description)
        
        if project_type in self.project_patterns:
            return self.project_patterns[project_type]['structure'].strip()
        
        # Default general structure
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

    def get_suggestions(self, description: str) -> Dict:
        analysis = self.analyze_prompt(description)
        structure = self.generate_structure(description)
        
        return {
            'detected_type': analysis['type'],
            'structure': structure,
            'confidence': analysis['confidence'],
            'matched_keywords': analysis['matched_keywords'],
            'score': analysis['score']
        }