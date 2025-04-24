const express = require("express");
const mongoose = require("mongoose");
const multer = require("multer");
const path = require("path");
const fs = require("fs");

const app = express();
app.use(express.json());
app.use("/uploads", express.static("uploads")); // Cho phép truy cập ảnh từ trình duyệt

mongoose.connect("mongodb://localhost:27017/mydatabase");

const ImageSchema = new mongoose.Schema({
  filename: String,        // tên file lưu trên server
  originalname: String,    // tên file gốc
  path: String,            // đường dẫn ảnh
  name: String             // tên do người dùng nhập
});

const Image = mongoose.model("Image", ImageSchema);

// Cấu hình Multer để lưu ảnh vào thư mục uploads/
const storage = multer.diskStorage({
  destination: "uploads/",
  filename: (req, file, cb) => {
    // Ưu tiên dùng tên người dùng nhập nếu có
    const ext = path.extname(file.originalname);
    const customName = req.body.name
      ? req.body.name.replace(/\s+/g, "_") + ext
      : file.originalname;
    cb(null, customName);
  },
});


const upload = multer({ storage });

// API upload ảnh
app.post("/upload", upload.single("image"), async (req, res) => {
  const customName = req.body.name || req.file.originalname;

  const newImage = new Image({
    filename: req.file.filename, 
    path: `/uploads/${req.file.filename}`,
  });

  await newImage.save();
  res.json(newImage);
});



// API lấy danh sách ảnh
app.get("/images", async (req, res) => {
  const images = await Image.find();
  res.json(images);
});

// API xoá ảnh theo id 
app.delete("/delete/:id", async (req, res) => {
  try {
    const image = await Image.findById(req.params.id);
    if (!image) {
      return res.status(404).json({ message: "Ảnh không tồn tại" });
    }

    // Xóa file khỏi thư mục uploads
    const filePath = `uploads/${image.filename}`;
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath); // Xóa file
    }

    // Xóa ảnh khỏi MongoDB
    await Image.findByIdAndDelete(req.params.id);

    res.json({ message: "Xóa ảnh thành công" });
  } catch (error) {
    res.status(500).json({ message: "Lỗi khi xóa ảnh", error });
  }
});

// Chạy server
app.listen(5000, () => console.log("Server running on port 5000"));
