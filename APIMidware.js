const express = require('express'); //웹 앱 프레임워크
const multer = require('multer'); //파일 처리 라이브러리
const axios = require('axios'); //HTTP require 관련 라이브러리
const FormData = require('form-data');
const fs = require('fs'); //file system
const path = require('path'); //file path

const app = express();
const upload = multer({ dest: 'uploads/' }); //임시 폴더

app.use(express.static('public')); //public/index.html 실행

app.post('/upload', upload.single('file'), async (req, res) => {
  try {
    const form = new FormData(); //파일 stream 을 만들어 전달
    form.append('file', fs.createReadStream(req.file.path), req.file.originalname);

    const response = await axios.post('http://localhost:8000/process', form, {
      headers: form.getHeaders()
    });

    fs.unlinkSync(req.file.path); //임시 파일 제거

    const resultText = response.data.result;
    //여기에 HTML을 넣어 /upload 화면 표시
    res.send(` 
      <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <title>Result</title>
      <style>
        body {
          font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
          background-color: #f5f7fa;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          margin: 0;
        }

        .result-container {
          background-color: #fff;
          border-radius: 16px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
          padding: 40px;
          text-align: center;
          width: 400px;
        }

        h1 {
          font-size: 24px;
          margin-bottom: 20px;
          color: #333;
        }

        .result-box {
          background-color: #f0f2f5;
          padding: 12px 24px;
          border-radius: 8px;
          font-size: 18px;
          margin-bottom: 20px;
          display: inline-block;
        }

        a {
          color: #4a90e2;
          text-decoration: none;
          font-weight: bold;
          font-size: 16px;
        }

        a:hover {
          text-decoration: underline;
        }
      </style>
    </head>
    <body>
      <div class="result-container">
        <h1>Examination Result</h1>
        <div class="result-box">${resultText}</div>
        <br />
        <a href="/">← Upload Another File</a>
      </div>
    </body>
    </html>
`);
  } catch (err) { //fastAPI 에서 전달한 에러 response
    if (err.response && err.response.data && err.response.data.detail) {
      res.status(err.response.status).send(`
        <h1>Error</h1>
        <pre>${err.response.data.detail}</pre>
        <a href="/">← Try Again</a>
      `); //fastAPI에서 받은 detail 값 사용
    } else {
      // 기타 에러 메세지
      res.status(500).send(`
        <h1>Unexpected Error</h1>
        <pre>${err.message}</pre>
        <a href="/">← Try Again</a>
      `);
    }
  }
  
});

app.listen(3000, () => { //서버 작동
  console.log('Express server listening on http://localhost:3000');
});
