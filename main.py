from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.utils import platform
from kivy.graphics import Color, Rectangle
import requests
import json
import os
import csv
from datetime import datetime

# Android storage setup
if platform == 'android':
    from android.storage import app_storage_path
    STORAGE_PATH = app_storage_path()
else:
    STORAGE_PATH = os.path.expanduser('~')

# Create directories
LESSONS_DIR = os.path.join(STORAGE_PATH, 'lessons')
AUDITS_DIR = os.path.join(STORAGE_PATH, 'audits')
os.makedirs(LESSONS_DIR, exist_ok=True)
os.makedirs(AUDITS_DIR, exist_ok=True)

# Bhashini API Credentials - YOUR VALID KEYS
ULCA_API_KEY = "C5JdA-yu4RNa5rAxrZeBtU766jEnseu9hSIU_904AFyphUbnyZgKAznCuwjOs2W6"
UDYAT_KEY = "29e35d7d18-b7ad-4c9b-8ffa-6b9fa0dbe413"

# Theme Colors
PINE_GREEN = (0.004, 0.475, 0.435, 1)
ACCENT_COLOR = (0.2, 0.6, 0.86, 1)


class BhashiniAPI:
    """Real Bhashini Translation API"""
    
    CONFIG_URL = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
    INFERENCE_URL = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
    
    def __init__(self):
        self.session = requests.Session()
        # Fallback dictionary for Khasi/Garo (if API doesn't support them)
        self.fallback_dict = {
            'hello': {'kha': 'Khublei', 'grt': 'Salaam'},
            'thank you': {'kha': 'Khublei shibun', 'grt': 'Mitela'},
            'teacher': {'kha': 'Kba sur', 'grt': 'Siksa'},
            'school': {'kha': 'Skul', 'grt': 'Iskul'},
            'student': {'kha': 'U sur', 'grt': 'Salsa'},
            'book': {'kha': 'Pothi', 'grt': 'Kitap'},
            'good morning': {'kha': 'Biang shaphang', 'grt': 'Nenggoripa'},
        }
    
    def get_config(self, source_lang, target_lang):
        """Get pipeline configuration from Bhashini"""
        try:
            payload = {
                "pipelineTasks": [{
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": source_lang,
                            "targetLanguage": target_lang
                        }
                    }
                }],
                "pipelineRequestConfig": {
                    "pipelineId": "64392f96daac500b55c543cd"
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "userID": UDYAT_KEY,
                "ulcaApiKey": ULCA_API_KEY
            }
            
            response = self.session.post(
                self.CONFIG_URL, 
                json=payload, 
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Config error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Config exception: {e}")
            return None
    
    def translate_with_api(self, text, source_lang, target_lang, service_id):
        """Call Bhashini inference API"""
        try:
            payload = {
                "pipelineTasks": [{
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": source_lang,
                            "targetLanguage": target_lang
                        },
                        "serviceId": service_id
                    }
                }],
                "inputData": {
                    "input": [{"source": text}]
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": ULCA_API_KEY
            }
            
            response = self.session.post(
                self.INFERENCE_URL,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'pipelineResponse' in result:
                    return result['pipelineResponse'][0]['output'][0]['target']
            
            print(f"Translation error: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"Translation exception: {e}")
            return None
    
    def translate_text(self, text, target_lang="kha"):
        """Main translation function with fallback"""
        text_lower = text.lower().strip()
        
        # Try fallback dictionary first (Khasi/Garo not in Bhashini)
        if text_lower in self.fallback_dict:
            return self.fallback_dict[text_lower][target_lang]
        
        # Try Bhashini API (for Hindi bridge, then explain to user)
        try:
            # Try getting config for Hindi (Khasi/Garo likely unavailable)
            config = self.get_config("en", "hi")
            
            if config and 'pipelineResponseConfig' in config:
                service_id = config['pipelineResponseConfig'][0]['config'][0]['serviceId']
                hindi_trans = self.translate_with_api(text, "en", "hi", service_id)
                
                if hindi_trans:
                    lang_name = 'Khasi' if target_lang == 'kha' else 'Garo'
                    return f"[{lang_name} via Hindi]: {hindi_trans}"
        except:
            pass
        
        # Final fallback
        lang_name = 'Khasi' if target_lang == 'kha' else 'Garo'
        return f"[{lang_name}] {text} (dictionary only)"


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        header = Label(
            text='[b]Vidyasetu[/b]\nEducation Bridge for Meghalaya',
            font_size='28sp',
            size_hint_y=0.25,
            markup=True,
            color=PINE_GREEN
        )
        
        btn_tutor = Button(
            text='📚 Vernacular Tutor',
            font_size='20sp',
            size_hint_y=0.2,
            background_color=PINE_GREEN,
            background_normal=''
        )
        btn_tutor.bind(on_press=self.go_to_tutor)
        
        btn_audit = Button(
            text='🏫 Infrastructure Audit',
            font_size='20sp',
            size_hint_y=0.2,
            background_color=ACCENT_COLOR,
            background_normal=''
        )
        btn_audit.bind(on_press=self.go_to_audit)
        
        btn_lessons = Button(
            text='💾 Offline Lessons',
            font_size='20sp',
            size_hint_y=0.2,
            background_color=(0.3, 0.3, 0.3, 1),
            background_normal=''
        )
        btn_lessons.bind(on_press=self.go_to_lessons)
        
        info = Label(
            text='AI-powered education for NE India',
            size_hint_y=0.1,
            font_size='14sp',
            color=(0.5, 0.5, 0.5, 1)
        )
        
        layout.add_widget(header)
        layout.add_widget(btn_tutor)
        layout.add_widget(btn_audit)
        layout.add_widget(btn_lessons)
        layout.add_widget(info)
        
        self.add_widget(layout)
    
    def go_to_tutor(self, instance):
        self.manager.current = 'tutor'
    
    def go_to_audit(self, instance):
        self.manager.current = 'audit'
    
    def go_to_lessons(self, instance):
        self.manager.current = 'lessons'


class TutorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.translator = BhashiniAPI()
        self.translations = {}
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint_y=0.08)
        back_btn = Button(text='← Back', size_hint_x=0.3, background_color=PINE_GREEN)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        title = Label(text='Vernacular Tutor', font_size='22sp', bold=True)
        header.add_widget(back_btn)
        header.add_widget(title)
        
        # Text input
        self.text_input = TextInput(
            hint_text='Try: hello, teacher, school, thank you',
            size_hint_y=0.2,
            multiline=True,
            font_size='16sp'
        )
        
        # Language buttons
        lang_box = BoxLayout(size_hint_y=0.08, spacing=5)
        btn_khasi = Button(
            text='Translate to Khasi',
            background_color=ACCENT_COLOR,
            font_size='16sp'
        )
        btn_khasi.bind(on_press=lambda x: self.translate('kha'))
        btn_garo = Button(
            text='Translate to Garo',
            background_color=ACCENT_COLOR,
            font_size='16sp'
        )
        btn_garo.bind(on_press=lambda x: self.translate('grt'))
        lang_box.add_widget(btn_khasi)
        lang_box.add_widget(btn_garo)
        
        # Translation result box with WHITE BACKGROUND
        trans_box = BoxLayout(size_hint_y=0.25, padding=10)
        with trans_box.canvas.before:
            Color(1, 1, 1, 1)
            self.trans_bg = Rectangle(pos=trans_box.pos, size=trans_box.size)
        trans_box.bind(pos=lambda obj, val: setattr(self.trans_bg, 'pos', val))
        trans_box.bind(size=lambda obj, val: setattr(self.trans_bg, 'size', val))
        
        self.translation_label = Label(
            text='Translation will appear here',
            color=(0, 0, 0, 1),
            font_size='18sp',
            halign='center',
            valign='middle'
        )
        self.translation_label.bind(size=self.translation_label.setter('text_size'))
        trans_box.add_widget(self.translation_label)
        
        # Save button
        btn_save = Button(
            text='💾 Save Lesson (Offline)',
            size_hint_y=0.08,
            background_color=(0.1, 0.6, 0.1, 1),
            font_size='16sp'
        )
        btn_save.bind(on_press=self.save_lesson)
        
        # Status
        self.status_label = Label(
            text='Ready to translate',
            size_hint_y=0.08,
            color=(0, 0.5, 0, 1),
            font_size='14sp'
        )
        
        layout.add_widget(header)
        layout.add_widget(self.text_input)
        layout.add_widget(lang_box)
        layout.add_widget(trans_box)
        layout.add_widget(btn_save)
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)
    
    def translate(self, target_lang):
        text = self.text_input.text.strip()
        if not text:
            self.status_label.text = '⚠️ Enter text first'
            return
        
        self.status_label.text = f'Translating to {target_lang.upper()}...'
        
        try:
            translation = self.translator.translate_text(text, target_lang)
            if translation:
                self.translations[target_lang] = translation
                lang_name = 'Khasi' if target_lang == 'kha' else 'Garo'
                self.translation_label.text = f'{lang_name}:\n{translation}'
                self.status_label.text = '✓ Translation successful!'
            else:
                self.status_label.text = '❌ Translation failed'
        except Exception as e:
            self.status_label.text = f'❌ Error: {str(e)[:30]}'

    def save_lesson(self, instance):
        if not self.translations:
            self.status_label.text = '⚠️ Translate first before saving'
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        lesson_file = os.path.join(LESSONS_DIR, f'lesson_{timestamp}.json')
        
        lesson_data = {
            'original': self.text_input.text,
            'translations': self.translations,
            'timestamp': timestamp
        }
        
        with open(lesson_file, 'w', encoding='utf-8') as f:
            json.dump(lesson_data, f, ensure_ascii=False, indent=2)
        
        self.status_label.text = f'✓ Saved! Check Offline Lessons'


class AuditScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        header = BoxLayout(size_hint_y=0.08)
        back_btn = Button(text='← Back', size_hint_x=0.3, background_color=PINE_GREEN)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        title = Label(text='Infrastructure Audit', font_size='22sp', bold=True)
        header.add_widget(back_btn)
        header.add_widget(title)
        
        info_label = Label(
            text='Report school infrastructure issues',
            size_hint_y=0.05,
            font_size='14sp'
        )
        
        self.school_input = TextInput(
            hint_text='School Name',
            size_hint_y=0.1,
            multiline=False,
            font_size='16sp'
        )
        self.village_input = TextInput(
            hint_text='Village/Location',
            size_hint_y=0.1,
            multiline=False,
            font_size='16sp'
        )
        self.problem_input = TextInput(
            hint_text='Problem Description',
            size_hint_y=0.3,
            multiline=True,
            font_size='16sp'
        )
        
        btn_submit = Button(
            text='📤 Submit Report',
            size_hint_y=0.1,
            background_color=(0.1, 0.6, 0.1, 1),
            font_size='18sp'
        )
        btn_submit.bind(on_press=self.submit_report)
        
        self.status_label = Label(
            text='Fill all fields to submit',
            size_hint_y=0.08,
            color=(0, 0.5, 0, 1),
            font_size='14sp'
        )
        
        layout.add_widget(header)
        layout.add_widget(info_label)
        layout.add_widget(self.school_input)
        layout.add_widget(self.village_input)
        layout.add_widget(self.problem_input)
        layout.add_widget(btn_submit)
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)
    
    def submit_report(self, instance):
        school = self.school_input.text.strip()
        village = self.village_input.text.strip()
        problem = self.problem_input.text.strip()
        
        if not school or not village or not problem:
            self.status_label.text = '⚠️ Fill all fields'
            return
        
        csv_file = os.path.join(AUDITS_DIR, 'audit_log.csv')
        file_exists = os.path.isfile(csv_file)
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Timestamp', 'School', 'Village', 'Problem'])
            writer.writerow([timestamp, school, village, problem])
        
        self.school_input.text = ''
        self.village_input.text = ''
        self.problem_input.text = ''
        self.status_label.text = '✓ Report submitted successfully!'


class LessonsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        header = BoxLayout(size_hint_y=0.08)
        back_btn = Button(text='← Back', size_hint_x=0.3, background_color=PINE_GREEN)
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        title = Label(text='Offline Lessons', font_size='22sp', bold=True)
        header.add_widget(back_btn)
        header.add_widget(title)
        
        scroll = ScrollView(size_hint=(1, 0.85))
        self.lessons_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.lessons_grid.bind(minimum_height=self.lessons_grid.setter('height'))
        scroll.add_widget(self.lessons_grid)
        
        btn_refresh = Button(
            text='🔄 Refresh',
            size_hint_y=0.07,
            background_color=PINE_GREEN,
            font_size='16sp'
        )
        btn_refresh.bind(on_press=self.load_lessons)
        
        layout.add_widget(header)
        layout.add_widget(scroll)
        layout.add_widget(btn_refresh)
        
        self.add_widget(layout)
    
    def on_enter(self):
        self.load_lessons(None)
    
    def load_lessons(self, instance):
        self.lessons_grid.clear_widgets()
        
        try:
            lesson_files = [f for f in os.listdir(LESSONS_DIR) if f.endswith('.json')]
            
            if not lesson_files:
                label = Label(
                    text='No lessons saved yet',
                    size_hint_y=None,
                    height=100,
                    font_size='16sp'
                )
                self.lessons_grid.add_widget(label)
                return
            
            for lesson_file in sorted(lesson_files, reverse=True)[:10]:
                lesson_path = os.path.join(LESSONS_DIR, lesson_file)
                
                with open(lesson_path, 'r', encoding='utf-8') as f:
                    lesson_data = json.load(f)
                
                card = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=100,
                    padding=10
                )
                
                with card.canvas.before:
                    Color(1, 1, 1, 1)
                    card_bg = Rectangle(pos=card.pos, size=card.size)
                card.bind(pos=lambda obj, val, bg=card_bg: setattr(bg, 'pos', val))
                card.bind(size=lambda obj, val, bg=card_bg: setattr(bg, 'size', val))
                
                timestamp = lesson_data.get('timestamp', 'Unknown')
                original = lesson_data.get('original', '')[:40]
                translations = lesson_data.get('translations', {})
                trans_text = '\n'.join([f"{k.upper()}: {v}" for k, v in translations.items()])
                
                info_label = Label(
                    text=f'{timestamp}\n{original}\n{trans_text}',
                    size_hint_y=1,
                    color=(0, 0, 0, 1),
                    font_size='14sp'
                )
                
                card.add_widget(info_label)
                self.lessons_grid.add_widget(card)
        
        except Exception as e:
            error_label = Label(text=f'Error: {str(e)}', size_hint_y=None, height=100)
            self.lessons_grid.add_widget(error_label)


class VidyasetuApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(TutorScreen(name='tutor'))
        sm.add_widget(AuditScreen(name='audit'))
        sm.add_widget(LessonsScreen(name='lessons'))
        return sm


if __name__ == '__main__':
    VidyasetuApp().run()
