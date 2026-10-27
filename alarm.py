"""Local Windows alarm. Python standard library only."""
import ctypes
from datetime import datetime, timedelta
from pathlib import Path
import re
import tkinter as tk
from tkinter import messagebox

SOUND = Path(__file__).resolve().with_name('war_thunder_rwr_alarm.mp3')


def next_alarm(value, now):
    if not re.fullmatch(r'\d{1,2}:\d{2}', value.strip()):
        raise ValueError('Nhập giờ dạng HH:MM, ví dụ 07:30.')
    hour, minute = map(int, value.strip().split(':'))
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError('Giờ từ 00–23, phút từ 00–59.')
    result = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return result if result > now else result + timedelta(days=1)


class Player:
    def __init__(self):
        self.api = ctypes.windll.winmm
        self.opened = False

    def command(self, command):
        output = ctypes.create_unicode_buffer(512)
        error = self.api.mciSendStringW(command, output, len(output), None)
        if error:
            detail = ctypes.create_unicode_buffer(512)
            self.api.mciGetErrorStringW(error, detail, len(detail))
            raise RuntimeError(detail.value or f'MCI error {error}')
        return output.value

    def play(self):
        self.stop()
        if not SOUND.is_file():
            raise FileNotFoundError(f'Không thấy file âm thanh: {SOUND}')
        self.command(f'open "{SOUND}" type mpegvideo alias wakeup')
        self.opened = True
        self.command('play wakeup repeat')

    def stop(self):
        if self.opened:
            self.command('close wakeup')
            self.opened = False


class Alarm:
    def __init__(self, root):
        self.root = root
        self.player = Player()
        self.target = None
        self.ringing = False
        root.title('Báo thức')
        root.geometry('430x340')
        root.resizable(False, False)
        root.configure(bg='#f3f4f6')
        root.protocol('WM_DELETE_WINDOW', self.close)
        self.clock = tk.Label(root, font=('Segoe UI', 30), bg='#f3f4f6')
        self.clock.pack(pady=(15, 5))
        tk.Label(root, text='Giờ báo thức (24 giờ)', bg='#f3f4f6', font=('Segoe UI', 11)).pack()
        self.time = tk.StringVar(value=(datetime.now() + timedelta(minutes=1)).strftime('%H:%M'))
        self.entry = tk.Entry(root, textvariable=self.time, justify='center', width=8, font=('Segoe UI', 24))
        self.entry.pack(pady=7)
        buttons = tk.Frame(root, bg='#f3f4f6')
        buttons.pack(pady=5)
        tk.Button(buttons, text='Đặt báo thức', command=self.arm, font=('Segoe UI', 12), width=14).pack(side='left', padx=4)
        tk.Button(buttons, text='TẮT', command=self.stop, bg='#b91c1c', fg='white', font=('Segoe UI', 12, 'bold'), width=10).pack(side='left', padx=4)
        tk.Button(root, text='Nghe thử', command=self.ring, font=('Segoe UI', 10)).pack(pady=4)
        self.status = tk.StringVar(value='Chưa đặt báo thức')
        tk.Label(root, textvariable=self.status, bg='#f3f4f6', font=('Segoe UI', 11), wraplength=410).pack(pady=6)
        tk.Label(root, text='Giữ app mở và loa bật. Không tắt máy / Sleep.', bg='#f3f4f6', fg='#555555').pack()
        self.tick()

    def keep_awake(self, enabled):
        # Prevent automatic sleep while armed; does not override manual Sleep/shutdown.
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000001 if enabled else 0x80000000)

    def arm(self):
        try:
            target = next_alarm(self.time.get(), datetime.now())
            if not SOUND.is_file():
                raise FileNotFoundError(f'Không thấy {SOUND.name}')
            self.stop()
            self.target = target
            self.keep_awake(True)
            self.status.set('Đã đặt: ' + target.strftime('%H:%M · %d/%m/%Y'))
        except (ValueError, OSError) as error:
            messagebox.showerror('Không đặt được báo thức', str(error))

    def ring(self):
        self.target = None
        try:
            self.player.play()
            self.ringing = True
            self.keep_awake(True)
            self.status.set('ĐANG BÁO THỨC — bấm TẮT để dừng')
            self.root.deiconify()
            self.root.lift()
            self.root.attributes('-topmost', True)
        except (RuntimeError, OSError) as error:
            self.stop()
            self.status.set('LỖI PHÁT ÂM THANH')
            self.root.bell()
            messagebox.showerror('Lỗi âm thanh', str(error))

    def stop(self):
        self.player.stop()
        self.target = None
        self.ringing = False
        self.keep_awake(False)
        self.root.attributes('-topmost', False)
        self.status.set('Đã tắt / chưa đặt báo thức')

    def tick(self):
        now = datetime.now()
        self.clock.config(text=now.strftime('%H:%M:%S'))
        if self.target is not None and now >= self.target:
            self.ring()
        self.root.after(250, self.tick)

    def close(self):
        if (self.target or self.ringing) and not messagebox.askyesno('Thoát?', 'Thoát sẽ hủy báo thức. Bạn muốn thoát?'):
            return
        self.stop()
        self.root.destroy()


if __name__ == '__main__':
    Alarm(tk.Tk()).root.mainloop()
