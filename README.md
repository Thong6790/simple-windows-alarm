# Báo thức local

## Cài và chạy trên máy bạn

1. Dùng **Windows 10/11**. Cài [Python 3.12](https://www.python.org/downloads/windows/)
   từ python.org, chọn **Add python.exe to PATH** và giữ thành phần Tcl/Tk.
2. Trên GitHub chọn **Code → Download ZIP**, giải nén toàn bộ thư mục.
3. Nhấp đúp **Mo Bao Thuc.vbs**, nhập giờ HH:MM rồi bấm **Đặt báo thức**.

Không cần pip, không cần Internet khi chạy. Giữ file MP3 cùng thư mục với
`alarm.py`. Nếu Windows chặn VBS hoặc mở không được, mở Terminal ngay trong
thư mục đã giải nén và chạy `python alarm.py` để xem lỗi.

## Cách dùng
Giờ đã qua sẽ được đặt cho ngày mai. Mỗi lần đặt chỉ báo một lần.
MP3 phát lặp liên tục đến khi bấm **TẮT**. Nút này cũng hủy lịch đang chờ.
**Nghe thử** phát lặp ngay; bấm **TẮT** để dừng, rồi đặt giờ lại.

Giữ app mở, bật loa và kiểm tra âm lượng bằng Nghe thử trước khi dùng.
App ngăn Windows tự Sleep trong lúc chờ/reng, nhưng không đánh thức máy
khi bạn chủ động Sleep, Hibernate hoặc tắt máy. Đóng app sẽ hủy lịch;
mở lại cần đặt giờ lại. Không có chạy nền khi app đã đóng.

Chạy bằng dòng lệnh trong thư mục app:

    python alarm.py

File `war_thunder_rwr_alarm.mp3` được đính kèm để chạy ngay. Âm thanh do người
dùng cung cấp; repo không tuyên bố sở hữu bản quyền âm thanh War Thunder.

Đã khảo sát https://github.com/casonova/Alarm-Clock . Repo đó dùng playsound
và vòng lặp chặn giao diện, chỉ phát một lần, không đáp ứng nút tắt.
Bản này được viết riêng bằng Tkinter và bộ phát MCI sẵn của Windows;
không sao chép mã repo, không cần tải/cài dependency.

Kiểm thử: `python -m unittest discover -v`.
