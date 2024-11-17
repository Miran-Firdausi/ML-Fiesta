# **Sandalwood Cultivation Query System**  

A robust conversational chatbot system for processing and understanding audio resources related to sandalwood cultivation. The project leverages **Automatic Speech Recognition (ASR)**, **Natural Language Processing (NLP)**, and **3D avatars** to provide an interactive and user-friendly experience for answering user queries in Kannada.  

![Screenshot 2024-11-17 224127](https://github.com/user-attachments/assets/00085d11-f4e1-445f-b19e-933d5bd33028)

---

## **Features**  
- **Kannada Speech Recognition**: Supports colloquial Kannada dialects for transcription and analysis.  
- **Speech-to-Text and Text-to-Speech Pipeline**: Converts user queries and responses seamlessly between text and audio.  
- **Advanced Vector Search**: GPU-accelerated FAISS database for fast and accurate document retrieval.  
- **Conversational Chatbot with 3D Avatar**: Provides real-time, interactive responses through a dynamic interface.  
- **Caching and Resource Management**: Optimized for reduced latency and high performance under heavy load.  

---

## **Project Architecture**  

### **Training and Development Phases**  

1. **Data Collection and Preprocessing**  
   - Scraped audio files from YouTube related to sandalwood cultivation.  
   - Preprocessed transcriptions for meaningful context and garbage removal.  

2. **Model Selection and Comparison**  
   - Compared multiple ASR models for handling colloquial Kannada speech.  
   - Selected **Spring Lab IIT Madras Model** for best performance.  

3. **Vector Database Creation**  
   - Vectorized the text data using various vectorizers.  
   - Created a GPU-accelerated FAISS database for efficient retrieval.  

4. **Generative AI for Query Responses**  
   - Combined retrieved documents and passed them into a Kannada-capable language model.  
   - Generated contextual responses for user queries.  

5. **Integration with 3D Avatar**  
   - Used Three.js for creating a talking 3D avatar interface that interacts with users in real-time.  

---

### **Runtime Phases**  

1. **User Interaction**  
   - Accepts Kannada speech queries through the frontend.  

2. **Query Processing**  
   - Transcribes speech using ASR.  
   - Retrieves relevant audio segments and documents from the FAISS vector database.  
   - Passes retrieved data to the language model to generate a response.  

3. **Response Delivery**  
   - Converts text responses to speech.  
   - Displays the response through the interactive 3D avatar interface.  

---

## **Tech Stack**  

### **Frontend**  
- **React.js**  
- **Three.js** (for 3D avatar interaction)  

### **Backend**  
- **Django** (REST APIs for processing queries)  

### **AI Models**  
- **ASR**: Spring Lab IIT Madras Model for Kannada speech transcription.  
- **Vectorizer**: FAISS (GPU-accelerated).  
- **LLM**: Gemini 1.5 Flash.  

---

## **Setup and Installation**  

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Miran-Firdausi/ML-Fiesta.git
   cd ML-Fiesta
   ```  

2. **Backend Setup**  
   - Navigate to the backend directory:  
     ```bash
     cd backend
     ```  
   - Create a virtual environment and install dependencies:  
     ```bash
     python -m venv venv  
     source venv/bin/activate  
     pip install -r requirements.txt  
     ```  
   - Run the backend server:  
     ```bash
     python manage.py runserver
     ```  

3. **Frontend Setup**  
   - Navigate to the frontend directory:  
     ```bash
     cd frontend
     ```  
   - Install dependencies and start the development server:  
     ```bash
     npm install  
     npm run dev  
     ```  

4. **Environment Variables**  
   - Create a `.env` file in the backend directory with the following keys:  
     ```plaintext
     GEMINI_API_KEY=your-gemini-api-key
     AZURE_SPEECH_API_KEY=your-azure-speehc-api-key
     ```  

---

## **Usage**  

1. Open the web interface in your browser.  
2. Use your microphone to ask questions in Kannada or enter text about sandalwood cultivation.  
3. Interact with the 3D avatar for responses.  

---

## **Future Enhancements**  
- **Multilingual Support**: Extend to other Indian languages.  
- **Mobile App Integration**: Bring the system to mobile app.  
- **Enhanced Dataset**: Incorporate more dialects for greater ASR accuracy.  

---

## **Contributors**  
- **Miran-Firdausi**: Full-Stack Developer
- **Advik Sharma**: Machine Learning Engineer  
- **Meet Shah**: Machine Learning Engineer
