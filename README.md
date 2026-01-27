# Vidyasetu - Bridging Educational Gaps in Northeast India

<div align="center">

![Platform](https://img.shields.io/badge/Platform-Android-green.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI-Powered Vernacular Education Platform for Meghalaya**

[Demo Video](#demo) • [Features](#features) • [Installation](#installation) • [Architecture](#architecture)

</div>

---

## 🎯 Problem Statement

### Education Challenges in Northeast India (Meghalaya)

The Northeast region of India, particularly Meghalaya, faces unique educational challenges:

1. **Language Barrier**: Over 80% of students in rural Meghalaya speak Khasi or Garo as their first language, but schools teach in English medium
2. **Digital Divide**: Poor internet connectivity in 60% of rural areas limits access to online learning resources
3. **Infrastructure Gap**: No standardized system for communities to report school infrastructure issues
4. **Resource Scarcity**: Limited availability of vernacular educational content

**Impact**: High dropout rates, poor learning outcomes, and widening educational inequality in NE India.

---

## 💡 Our Solution: Vidyasetu

**Vidyasetu** (विद्या सेतु - "Bridge of Knowledge") is an offline-first mobile application that empowers students, teachers, and communities in Meghalaya through:

- **Vernacular Translation**: Real-time English-to-Khasi and English-to-Garo translation for educational content
- **Offline Learning**: Save and access lessons without internet connectivity
- **Community Infrastructure Reporting**: Enable villages to report school infrastructure issues directly

### Regional Relevance to NER

- **Language Support**: Focuses on Khasi and Garo, two major tribal languages of Meghalaya
- **Offline-First Design**: Works in low-connectivity areas common in NE hill regions
- **Community-Driven**: Aligns with traditional Meghalayan community governance systems
- **Culturally Sensitive**: Respects and preserves indigenous languages

---

## ✨ Features

### 📚 Vernacular Tutor

Transform education through native language support:

- **Dual Language Support**: English → Khasi and English → Garo translation
- **Educational Focus**: 100+ curated phrases covering school subjects
- **AI-Powered**: Bhashini API integration for accurate translation
- **Smart Fallback**: Dictionary-based translation when offline or API unavailable
- **Real-Time Display**: Instant translation results

**Use Cases**:
- Teachers explaining concepts in local languages
- Students understanding homework in native tongue
- Parents helping children with studies

### 💾 Offline Lessons Library

Learn anywhere, anytime:

- **Save Translations**: Store lessons locally on device
- **Zero Internet Required**: Access saved content offline
- **Organized Storage**: JSON-based lesson management
- **Quick Refresh**: View all saved lessons instantly

**Impact**: Students in remote villages can study without connectivity

### 🏫 Infrastructure Audit Tool

Empower communities to improve schools:

- **Simple Reporting**: Report infrastructure issues (electricity, toilets, furniture, etc.)
- **Data Collection**: Structured CSV export for analysis
- **Community Voice**: Direct channel from villages to authorities
- **Trackable**: Timestamped records of all reports

**Use Cases**:
- Village leaders reporting broken infrastructure
- Teachers documenting facility needs
- Government tracking rural school conditions

---

## 🛠️ Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Kivy 2.2.1 | Cross-platform mobile UI |
| **Language** | Python 3.11 | Application logic |
| **Translation API** | Bhashini (Govt of India) | Neural translation engine |
| **Storage** | JSON + CSV | Offline data persistence |
| **Build System** | Buildozer | Android APK packaging |

### AI/ML Components

- **Bhashini NMT Models**: Neural Machine Translation for Indian languages
- **Dictionary Fallback**: 100+ curated Khasi/Garo educational phrases
- **Hybrid Approach**: API-first with intelligent offline fallback

### Why These Choices?

1. **Kivy**: Single codebase deploys to Android, iOS, and Desktop
2. **Python**: Rapid development with extensive AI/ML libraries
3. **Bhashini**: Government-backed, free, and focused on Indian languages
4. **Offline-First**: JSON/CSV storage works without internet

---

## 📱 Installation

### For Users (APK Download)

1. Download `vidyasetu.apk` from [Releases](https://github.com/yourusername/vidyasetu/releases)
2. Enable "Install from Unknown Sources" in Android settings
3. Install APK
4. Open Vidyasetu app

### For Developers

#### Prerequisites

```bash
Python 3.11+
Android SDK 28+
Java JDK 8+
Git
