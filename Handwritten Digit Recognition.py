import tkinter as tk
from tkinter import messagebox
from tkinter import Canvas, Button
from sklearn import datasets, svm
import numpy as np
from PIL import Image, ImageDraw
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# Load the digits dataset from sklearn
digits = datasets.load_digits()
X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.2, random_state=42)

# Train the Support Vector Machine (SVM) model
clf = SVC(kernel='linear')
clf.fit(X_train, y_train)

# Evaluate the model on the test set
accuracy = clf.score(X_test, y_test)
print("Model Accuracy on Test Set:", accuracy)


# Create the GUI
class DigitRecognizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Digit Recognizer")

        self.canvas = Canvas(master, width=200, height=200, bg="white")
        self.canvas.grid(row=0, columnspan=2)

        self.predict_button = Button(master, text="Predict Digit", command=self.predict_digit)
        self.predict_button.grid(row=1, column=0)

        self.clear_button = Button(master, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.grid(row=1, column=1)

        self.drawing = False
        self.canvas.bind("<Motion>", self.draw)
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        self.image = Image.new("L", (200, 200), 0)
        self.draw = ImageDraw.Draw(self.image)

    def start_draw(self, event):
        self.drawing = True

    def stop_draw(self, event):
        self.drawing = False

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            r = 8
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")
            self.draw.ellipse([x - r, y - r, x + r, y + r], fill="white")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (200, 200), 0)
        self.draw = ImageDraw.Draw(self.image)

    def predict_digit(self):
        if np.sum(np.array(self.image)) == 0:
            messagebox.showwarning("Warning", "Draw a digit before predicting.")
        else:
            # Resize the image to 8x8
            resized_image = self.image.resize((8, 8))
            # Convert the image to grayscale
            grayscale_image = resized_image.convert('L')
            # Convert the image to a numpy array
            digit_array = np.array(grayscale_image)
            # Flatten the array
            digit_array = digit_array.flatten()

            # Debugging: Print the resized and flattened digit array
            print("Flattened digit array:", digit_array)

            # Debugging: Display the resized digit image
            resized_image.show()

            # Predict the digit using the model
            predicted_digit = clf.predict([digit_array])
            
            # Debugging: Print the predicted digit
            print("Predicted digit:", predicted_digit[0])
            
            messagebox.showinfo("Prediction", f"The drawn digit is: {predicted_digit[0]}")


def main():
    root = tk.Tk()
    app = DigitRecognizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
