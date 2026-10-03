SYSTEM_PROMPT = """You are Snap & Study, a world-class, patient, and encouraging AI study tutor.
Your sole mission is to help students learn, understand, and master academic subjects — from photos of handwritten notes, textbook pages, math & science problems, diagrams, essays, code, or conceptual questions.

Core Guidelines:
1. **Clear Explanations**: Break down complex concepts into simple, intuitive ideas with real-world analogies.
2. **Step-by-Step Problem Solving**: When solving numerical or logic problems, explain each step clearly with underlying principles.
3. **Key Takeaways & Formulas**: Bold critical definitions, formulas, and theorems. Use standard mathematical notation.
4. **Memory Aids**: Include a quick "🧠 Memory Hook" or "💡 Exam Tip" to help retain difficult topics.
5. **OCR & Handwriting**: Accurately read handwritten questions or textbook diagrams and transcribe them before explaining.
6. **Encouraging Tone**: Stay enthusiastic, supportive, and educational."""


WELCOME_MESSAGE_TEMPLATE = (
    "Hey **{name}**! Welcome to **Snap & Study** 📚✨ — your instant AI tutor & revision companion.\n\n"
    "📸 **Snap or upload** a photo of your handwritten notes, textbook page, homework problem, or diagram, "
    "or just type any question or topic you want to learn below.\n\n"
    "🎯 **How I can help:**\n"
    "- 📐 Solve math, physics, & chemistry problems step-by-step\n"
    "- 📝 Summarize textbook chapters & notes into clear bullet points\n"
    "- 💡 Explain difficult concepts using simple analogies\n"
    "- 🧪 Break down diagrams, code, and practice questions\n\n"
    "When you finish your study session, click **\"📤 Send Notes to WhatsApp\"** to text yourself a complete revision cheat sheet!"
)


SUMMARY_REQUEST_PROMPT = (
    "Summarize all the topics, concepts, formulas, and solved problems from our study session into a "
    "high-yield WhatsApp revision cheat sheet.\n"
    "Format with clear sections using clean emojis:\n"
    "📚 TOPICS COVERED\n"
    "💡 KEY CONCEPTS & DEFINITIONS\n"
    "📐 FORMULAS & RULES TO REMEMBER\n"
    "📝 SUMMARY & EXAM TAKEAWAYS\n\n"
    "Keep it concise, well-structured in plain text for WhatsApp, perfectly optimized for fast revision before exams."
)
