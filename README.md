# 🎙️ Deep Learning Text-to-Speech Web Application

## Overview

This project is a **production-oriented Text-to-Speech (TTS) web application**
built using **deep learning**, modern web technologies, and cloud infrastructure.

The goal is **not** to create a simple notebook demo, but to design, implement,
deploy, and iterate on a **real AI-powered product**, covering the full lifecycle
of an AI system in production:

- model evaluation and deployment,
- API design,
- frontend integration,
- infrastructure and DevOps,
- user management and monetization.

The application allows users to input text, generate speech using a neural TTS
model, listen to the audio directly in the browser, and download the result.

---

## 🎯 Project Objectives

This project is driven by three complementary goals:

### 1️⃣ Pedagogical Objective (Primary)

Learn **how real AI products are built and operated**, including:

- serving deep learning models in production,
- designing scalable architectures,
- handling latency, cost, and infrastructure constraints,
- securing and exposing APIs,
- understanding trade-offs between managed services and self-hosted solutions.

### 2️⃣ Portfolio & Career Objective

Build a **serious, professional project** that:

- can be showcased to recruiters,
- demonstrates end-to-end AI engineering skills,
- adds strong value to a CV or LinkedIn profile,
- can be confidently explained in technical interviews.

### 3️⃣ Product / Business Objective (Optional)

Design the system so that it **could evolve into a real product**, with:

- user accounts,
- quotas and billing,
- premium features,
- long-term extensibility.

Profitability is a bonus, not the primary constraint.

---

## ✨ Features

### MVP (Free / Anonymous Users)

- Intuitive text input interface
- Secure transmission (HTTPS)
- Text-to-speech generation using a neural model
- Audio playback directly in the browser
- Audio file download
- No account required
- Character-based daily quota

### Premium Features (Later Stages)

- User authentication and account management
- Higher usage limits
- Additional voices
- Voice cloning
- Payment system (Stripe)

---

## 🧠 Model Strategy

- **Kokoro v0.19** for MVP text-to-speech
- **XTTS v2 / OpenVoice** for voice cloning (later)

The system is designed with **model abstraction** so models can be swapped
without rewriting the application.

---

## 🏗️ Architecture Overview

The application follows a **service-oriented architecture**:

- **React + Vite** frontend
- **Express.js** backend (business logic, orchestration)
- **FastAPI** inference service for TTS
- **MongoDB Atlas** for data
- **Amazon S3** for audio storage
- **VPS + EC2** deployment model

👉 Full architecture documentation is available in the
[`docs/`](./docs) folder.

---

## 📚 Documentation

Detailed technical and product documentation lives in the
[`docs/`](./docs) directory, including:

- architecture diagrams,
- security boundaries,
- request flows,
- deployment views,
- product scope and roadmap.

Start here:
➡️ **[Documentation Index](./docs/README.md)**

---

## 📌 Status

🚧 In active development — evolving iteratively as new features are added.

---

## 🚀 Next Steps

- Local validation of the TTS model
- API exposure via FastAPI
- Frontend MVP
- Cloud deployment
