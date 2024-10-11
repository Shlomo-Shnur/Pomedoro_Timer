import tkinter
from os import path

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CANVAS_WIDTH = 200
CANVAS_HEIGHT = 224
CHECK_MARK = "✔"
ONE_SECOND = 1000
ONE_MINUTE_TO_SECONDS = 60

# ---------------------------- GLOBALS ------------------------------- #
repetition = 1
timer = ""
current_path = path.dirname(path.realpath(__file__))


def app():
    def bring_to_front():
        """Brings the canvas screen to the front of the monitor if it got minimized or overlapped"""
        screen.deiconify()
        screen.lift()
        screen.focus_force()
        screen.attributes("-topmost", True)
        screen.attributes("-topmost", False)

    # ---------------------------- TIMER RESET ------------------------------- #
    def reset_timer():
        """Resets the canvas to initial state when the timer is opened, no check marks, timer is 00:00"""
        global repetition
        screen.after_cancel(timer)
        timer_format = f"00:00"
        canvas.itemconfig(timer_text, text=timer_format)
        title_label.config(text="Timer", fg=GREEN)
        check_mark_label.config(text="")
        repetition = 1

    # ---------------------------- TIMER MECHANISM ------------------------------- #
    def start_timer():
        """Starts the count-down, switches between states according to the repetition number"""
        global repetition
        work_seconds = WORK_MIN * ONE_MINUTE_TO_SECONDS
        short_break_seconds = SHORT_BREAK_MIN * ONE_MINUTE_TO_SECONDS
        long_break_seconds = LONG_BREAK_MIN * ONE_MINUTE_TO_SECONDS
        if repetition == 8:
            total_seconds = long_break_seconds
            repetition = 1
            title_label.config(text="Break", fg=RED)
            bring_to_front()
        elif repetition % 2 == 0:
            total_seconds = short_break_seconds
            title_label.config(text="Break", fg=PINK)
            repetition += 1
            bring_to_front()
        else:
            total_seconds = work_seconds
            title_label.config(text="Work", fg=GREEN)
            repetition += 1
        count_down(total_seconds)

    # ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
    def count_down(total_seconds):
        """Timer's count down function, counts down until 0 and adds check marks after each work cycle is done"""
        global timer
        minutes, seconds = divmod(total_seconds, ONE_MINUTE_TO_SECONDS)
        timer_format = f"{minutes:02}:{seconds:02}"
        canvas.itemconfig(timer_text, text=timer_format)
        if total_seconds > 0:
            timer = screen.after(ONE_SECOND, count_down, total_seconds - 1)
        else:
            check_mark_duplicates = repetition // 2 * CHECK_MARK
            check_mark_label.config(text=check_mark_duplicates)
            start_timer()

    # ---------------------------- UI SETUP ------------------------------- #
    # screen setup
    screen = tkinter.Tk()
    screen.title("Pomodoro")
    screen.config(padx=100, pady=50, bg=YELLOW)

    # canvas and image setup
    canvas = tkinter.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=YELLOW, highlightthickness=0)
    tomato_image = tkinter.PhotoImage(file=path.join(current_path + "\\tomato.png"))
    canvas.create_image(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, image=tomato_image)
    timer_text = canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 + 18, text="00:00", fill="white",
                                    font=(FONT_NAME, 35, "bold"))
    canvas.grid(column=1, row=1)

    # Timer label
    title_label = tkinter.Label(text="Timer", font=(FONT_NAME, 50), fg=GREEN, bg=YELLOW)
    title_label.grid(column=1, row=0)

    # Button to start the timer
    start_button = tkinter.Button(text="Start", highlightthickness=0, command=start_timer)
    start_button.grid(column=0, row=2)

    # Button to reset the timer
    reset_button = tkinter.Button(text="Reset", highlightthickness=0, command=reset_timer)
    reset_button.grid(column=2, row=2)

    # Placeholder for the check marks to come ahead after each work cycle
    check_mark_label = tkinter.Label(font=(10,), fg=GREEN, bg=YELLOW)
    check_mark_label.grid(column=1, row=3)

    screen.mainloop()


if __name__ == "__main__":
    app()
