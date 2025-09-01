# 📌 Task Management Backend

Backend API cho hệ thống quản lý **Task**  
Công nghệ: **FastAPI + SQLAlchemy + PostgreSQL**  
Hỗ trợ:
- Authentication bằng **JWT**
- Quản lý **Project, Task, Comment, Attachment (upload file)**
- Báo cáo

---

## 🚀 Yêu cầu hệ thống

- Windows 10/11  
- Python 3.12+  
- PostgreSQL 16+  

---

## ⚙️ Cài đặt

### 1. Clone source code
```bash
git clone https://github.com/manhdao1006/be-assignment.aug-2025.git
cd task-management
```
### 2. Tạo virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows

Sau khi chạy lệnh trên, sẽ thấy `(venv)` xuất hiện trong CMD/PowerShell.
```
### 3. Cài dependencies
```bash
pip install -r requirements.txt
```
### 4. Tạo database
Mở **pgAdmin** hoặc **psql**, chạy lệnh:

```sql
CREATE DATABASE task_management;
```
### 5. Chạy migration
```bash
alembic upgrade head
```
### ▶️ Chạy server

Trong CMD/PowerShell (vẫn trong virtualenv):

```bash
uvicorn app.main:app --reload
```
- API chạy ở: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

---

## 📂 Upload file

- File đính kèm được lưu trong thư mục `uploads/`  
- Giới hạn:
  - Tối đa **5MB / file**
  - Tối đa **3 file / task**

---

## ✅ Test nhanh API

1. Mở [Swagger UI](http://127.0.0.1:8000/docs)  
2. Đăng nhập, lấy **JWT token**  
3. Thử gọi các API:
   - **Project**
   - **Task**
   - **Comment**
   - **Attachment**
