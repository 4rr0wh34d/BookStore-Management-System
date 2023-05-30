import tkinter as tk


class Calculator23:

    def __init__(self, new_frame):
        self.frame = new_frame
        self.temp1 = 0
        self.temp2 = 0
        self.total_value = 0
        self.operand = ''
        self.operation_status = False
        self.no_append = False
        self.operate = {'+': lambda a, b: a + b,
                        '-': lambda a, b: a - b,
                        'x': lambda a, b: a * b,
                        '/': lambda a, b: a / b,
                        '//': lambda a, b: a // b}

        calculator = [['AC', '-/+', '%', '//'],
                      ['1', '2', '3', '+'],
                      ['4', '5', '6', '-'],
                      ['7', '8', '9', 'x'],
                      ['.', '0', '=', '/']]

        # self.frame = tk.Frame(self.root)
        self.text_result = tk.Text(self.frame, height=2, width=40)

        self.text_result.grid(row=0, columnspan=4, sticky=tk.E + tk.W, padx=5, pady=5)

        for i in range(5):
            for j in range(4):
                self.button = tk.Button(self.frame, text=calculator[i][j], width=10, height=2)
                self.button.configure(command=lambda value=calculator[i][j]: self.handle_calculation(value))
                self.button.grid(row=i + 1, column=j, sticky=tk.NSEW)

        # self.frame.pack(fill='both')
        # self.root.mainloop()

    def handle_calculation(self, choice):

        operation = ['+', '-', 'x', '/', '=', '//']

        # if the argument choice passed is between 1 and 9
        if '0' <= choice <= '9' or choice == '.':
            # check if any operand has already been pressed
            if self.operation_status:
                # Deleting the previous input after operand has been pressed. It is only done once to avoid
                # multiple input from being reset every time.
                if self.no_append:
                    self.text_result.delete('1.0', 'end')
                    self.no_append = False
                self.text_result.insert('end', choice)

            else:
                self.text_result.insert('end', choice)

        # Checking if the operand has been pressed
        elif choice in operation:

            # checking if there is any operation from before
            if self.operation_status:
                # storing second input into temp2 variable
                self.temp2 = float(self.text_result.get('1.0', 'end'))

                # calculating total output of an operation using lambda function inside dictionary
                self.total_value = self.operate[self.operand](self.temp1, self.temp2)
                self.text_result.delete('1.0', 'end')

                # Checking if there is any number after decimal point
                remainder = self.total_value % 1
                if remainder == 0:
                    self.total_value = int(self.total_value)

                # Displaying total result
                self.text_result.insert('end', str(self.total_value))
                self.temp1 = self.total_value  # Storing result in temp1 variable for further calculation

                # If the input is = sign then reset operand and operation_status value
                if choice == '=':
                    self.operand = ''
                    self.operation_status = False

                else:
                    self.operand = choice
                    # Setting boolean value no_append to True so that any previous input is cleared before getting
                    # new input
                    self.no_append = True

            else:
                if choice == '-':
                    self.text_result.insert('end', '-')
                    self.operation_status = False
                else:
                    self.temp1 = float(self.text_result.get('1.0', 'end'))
                    self.operand = choice
                    self.operation_status = True
                    self.no_append = True

        elif choice == 'AC':
            self.text_result.delete('1.0', 'end')
            self.temp1 = 0
            self.temp2 = 0
            self.total_value = 0
            self.operand = ''

        elif choice == '%':
            self.temp1 = float(self.text_result.get('1.0', 'end')) * 0.01
            self.text_result.delete('1.0', 'end')
            self.text_result.insert('end', str(self.temp1))

        # Changing to positive or negative input
        elif choice == '-/+':
            value = self.text_result.get('1.0', 'end')
            if value[0] == '-':
                value.replace('-', '')

            else:
                value = ''.join(('-', value))

            self.text_result.delete('1.0', 'end')
            self.text_result.insert('end', value)


def main():
    root = tk.Tk()
    frame = tk.Frame(root)
    calc = Calculator23(frame)
    frame.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
