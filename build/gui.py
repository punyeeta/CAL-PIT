from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, messagebox, filedialog
import pyglet, os
import subprocess
from tkinter import font as tkFont
import sympy as sp
from scipy import integrate
import numpy as np
from integration import parse_user_function, process_user_integration
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
import re

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()
# Define relative paths from the script directory
ASSETS_DIR = SCRIPT_DIR / "assets" / "frame0"
FONTS_DIR = SCRIPT_DIR / "assets" / "fonts"

# Load the Poppins font using a relative path
font_path = FONTS_DIR / "Poppins-Medium.ttf"
if font_path.exists():
    pyglet.font.add_file(str(font_path))
else:
    print(f"Warning: Font file not found at {font_path}")

def relative_to_assets(path: str) -> Path:
    """Convert a relative path to an absolute path within the assets directory"""
    return ASSETS_DIR / path

window = Tk()

window.geometry("1440x1024")
window.configure(bg = "#4268FB")
window.title("f'prime")

# Set the window icon
icon_path = SCRIPT_DIR / "icon.ico"
if icon_path.exists():
    window.iconbitmap(str(icon_path))
else:
    print(f"Warning: Icon file not found at {icon_path}")

poppins_medium = tkFont.Font(family="Poppins", size=10)

# Define text color
TEXT_COLOR = "#273C8B"

def add_placeholder(widget, placeholder_text, is_entry=True):
    """Add placeholder functionality to Entry or Text widgets with Poppins font"""
    
    # Create font object - use the exact name that worked in your test
    poppins_font = tkFont.Font(family="Poppins Medium", size=10)
    
    # Apply the font directly
    if is_entry:
        widget.config(font=poppins_font)
    else:
        widget.config(font=poppins_font)
    
    # Rest of placeholder functionality
    if is_entry:
        # For Entry widgets
        widget.insert(0, placeholder_text)
        widget.config(fg='gray')
        
        def on_entry_focus_in(event):
            if widget.get() == placeholder_text:
                widget.delete(0, "end")
                widget.config(fg=TEXT_COLOR, font=poppins_font)  # Re-apply font with custom color
        
        def on_entry_focus_out(event):
            if widget.get() == "":
                widget.insert(0, placeholder_text)
                widget.config(fg='gray', font=poppins_font)  # Re-apply font
                
        widget.bind("<FocusIn>", on_entry_focus_in)
        widget.bind("<FocusOut>", on_entry_focus_out)
    else:
        # For Text widgets
        widget.insert("1.0", placeholder_text)
        widget.config(fg='gray')
        
        def on_text_focus_in(event):
            if widget.get("1.0", "end-1c") == placeholder_text:
                widget.delete("1.0", "end")
                widget.config(fg=TEXT_COLOR, font=poppins_font)  # Re-apply font with custom color
        
        def on_text_focus_out(event):
            if widget.get("1.0", "end-1c") == "":
                widget.insert("1.0", placeholder_text)
                widget.config(fg='gray', font=poppins_font)  # Re-apply font
                
        widget.bind("<FocusIn>", on_text_focus_in)
        widget.bind("<FocusOut>", on_text_focus_out)

canvas = Canvas(
    window,
    bg = "#4268FB",
    height = 1024,
    width = 1440,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    720.0,
    512.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    719.0,
    511.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    722.0,
    178.99966430664062,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    95.0,
    96.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    668.0,
    354.0,
    image=image_image_5
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    668.5,
    354.0,
    image=entry_image_1
)
#Input Function Entry
entry_1 = Entry(
    bd=0,
    bg="#F3F3F3",
    fg=TEXT_COLOR,
    highlightthickness=0
)
entry_1.place(
    x=483.0,
    y=337.0,
    width=371.0,
    height=32.0
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    325.0,
    477.0,
    image=image_image_6
)

#FirstDerivativeResult
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    325.5,
    477.0,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#F3F3F3",
    fg=TEXT_COLOR,
    highlightthickness=0
)
entry_2.place(
    x=140.0,
    y=460.0,
    width=371.0,
    height=32.0
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    761.0,
    477.0,
    image=image_image_7
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    761.5,
    477.0,
    image=entry_image_3
)

#NumericalIntegrationResult
entry_3 = Text(
    bd=0,
    bg="#F3F3F3",
    fg=TEXT_COLOR,
    highlightthickness=0
)
entry_3.place(
    x=576.0,
    y=460.0,
    width=371.0,
    height=32.0
)

# Create frames for the graphs
graph_frame_1 = Frame(window, bg="#4268FB", width=300, height=300)
graph_frame_1.place(relx=0.112, rely=0.572, anchor="nw")

graph_frame_2 = Frame(window, bg="#4268FB", width=300, height=300)
graph_frame_2.place(relx=0.4, rely=0.572, anchor="nw")

graph_frame_3 = Frame(window, bg="#4268FB", width=300, height=300)
graph_frame_3.place(relx=0.682, rely=0.572, anchor="nw")

# Create matplotlib figures for the graphs
fig1 = Figure(figsize=(3, 3), dpi=100, facecolor="#3159EE")
ax1 = fig1.add_subplot(111)
ax1.set_facecolor("#3159EE")
ax1.grid(True, linestyle='--', alpha=0.7, color='white')
ax1.axhline(y=0, color='white', linestyle='-', alpha=0.3)
ax1.axvline(x=0, color='white', linestyle='-', alpha=0.3)
ax1.set_title('Original Function', fontsize=10, color='white')
ax1.set_xlabel('x', fontsize=8, color='white')
ax1.set_ylabel('f(x)', fontsize=8, color='white')
ax1.tick_params(colors='white')
ax1.spines['top'].set_color('white')
ax1.spines['right'].set_color('white')
ax1.spines['bottom'].set_color('white')
ax1.spines['left'].set_color('white')

fig2 = Figure(figsize=(3, 3), dpi=100, facecolor="#3159EE")
ax2 = fig2.add_subplot(111)
ax2.set_facecolor("#3159EE")
ax2.grid(True, linestyle='--', alpha=0.7, color='white')
ax2.axhline(y=0, color='white', linestyle='-', alpha=0.3)
ax2.axvline(x=0, color='white', linestyle='-', alpha=0.3)
ax2.set_title('First Derivative', fontsize=10, color='white')
ax2.set_xlabel('x', fontsize=8, color='white')
ax2.set_ylabel('f\'(x)', fontsize=8, color='white')
ax2.tick_params(colors='white')
ax2.spines['top'].set_color('white')
ax2.spines['right'].set_color('white')
ax2.spines['bottom'].set_color('white')
ax2.spines['left'].set_color('white')

fig3 = Figure(figsize=(3, 3), dpi=100, facecolor="#3159EE")
ax3 = fig3.add_subplot(111)
ax3.set_facecolor("#3159EE")
ax3.grid(True, linestyle='--', alpha=0.7, color='white')
ax3.axhline(y=0, color='white', linestyle='-', alpha=0.3)
ax3.axvline(x=0, color='white', linestyle='-', alpha=0.3)
ax3.set_title('Integral', fontsize=10, color='white')
ax3.set_xlabel('x', fontsize=8, color='white')
ax3.set_ylabel('∫f(x)dx', fontsize=8, color='white')
ax3.tick_params(colors='white')
ax3.spines['top'].set_color('white')
ax3.spines['right'].set_color('white')
ax3.spines['bottom'].set_color('white')
ax3.spines['left'].set_color('white')

# Create canvas widgets for the graphs
canvas1 = FigureCanvasTkAgg(fig1, master=graph_frame_1)
canvas1.draw()
canvas1.get_tk_widget().pack(fill='both', expand=True)

canvas2 = FigureCanvasTkAgg(fig2, master=graph_frame_2)
canvas2.draw()
canvas2.get_tk_widget().pack(fill='both', expand=True)

canvas3 = FigureCanvasTkAgg(fig3, master=graph_frame_3)
canvas3.draw()
canvas3.get_tk_widget().pack(fill='both', expand=True)

# Function to compute numerical derivative
def numerical_derivative(func, x, h=0.0001):
    """Compute derivative using central difference method"""
    return (func(x + h) - func(x - h)) / (2 * h)

# Function to update the graphs
def update_graphs(func_str=None):
    # Default function if none provided
    if func_str is None or func_str == "" or func_str == "Enter your function here":
        func_str = "x^2 + 2x + 1"
    
    try:
        # Parse the function using our enhanced parser
        func = parse_user_function(func_str)
        
        # Initialize bounds
        x_min, x_max = -5, 5  # Fixed graph range
        integration_bounds = None
        
        # Get the lower and upper limits
        try:
            lower_limit = float(entry_4.get())
            upper_limit = float(entry_5.get())
            integration_bounds = (lower_limit, upper_limit)
        except:
            pass
        
        # Create x values for the full graph range
        x_values = np.linspace(x_min, x_max, 1000)
        
        # Compute function values
        y_values = [func(x_val) for x_val in x_values]
        
        # Calculate y-axis bounds based on function values
        y_min = min(y_values) - 1
        y_max = max(y_values) + 1
        
        # Get the derivative expression from the text field
        derivative_text = entry_2.get("1.0", "end-1c")
        derivative_expr = None
        
        # Extract the derivative expression from the text
        if "d/dx" in derivative_text and "=" in derivative_text:
            derivative_expr = derivative_text.split("=")[1].strip()
            try:
                # Parse the derivative expression
                derivative_func = parse_user_function(derivative_expr)
                # Compute derivative values
                y_prime = [derivative_func(x_val) for x_val in x_values]
            except:
                # Fallback to numerical derivative if parsing fails
                y_prime = np.array([numerical_derivative(func, xi) for xi in x_values])
        else:
            # Fallback to numerical derivative if text doesn't contain derivative
            y_prime = np.array([numerical_derivative(func, xi) for xi in x_values])
        
        # Calculate y-axis bounds for derivative
        y_prime_min = min(y_prime) - 1
        y_prime_max = max(y_prime) + 1
        
        # Get the integral expression from the text field
        integral_text = entry_3.get("1.0", "end-1c")
        integral_expr = None
        
        # Extract the integral expression from the text
        if "∫" in integral_text and "dx" in integral_text and "=" in integral_text:
            # Get the first line which contains the indefinite integral
            first_line = integral_text.split("\n")[0]
            integral_expr = first_line.split("=")[1].strip()
            # Remove "+ C" if present
            if "+ C" in integral_expr:
                integral_expr = integral_expr.replace("+ C", "").strip()
            
            try:
                # Parse the integral expression
                integral_func = parse_user_function(integral_expr)
                # Compute integral values
                y_integral = [integral_func(x_val) for x_val in x_values]
            except:
                # Fallback to numerical integration if parsing fails
                y_integral = np.zeros_like(x_values)
                for i in range(1, len(x_values)):
                    y_integral[i], _ = integrate.quad(func, x_min, x_values[i])
        else:
            # Fallback to numerical integration if text doesn't contain integral
            y_integral = np.zeros_like(x_values)
            for i in range(1, len(x_values)):
                y_integral[i], _ = integrate.quad(func, x_min, x_values[i])
        
        # Calculate y-axis bounds for integral
        y_integral_min = min(y_integral) - 1
        y_integral_max = max(y_integral) + 1
        
        # Convert expressions to LaTeX format for display using sympy
        try:
            x = sp.Symbol('x')
            # Convert the function string to sympy format for LaTeX
            sympy_str = func_str.replace('^', '**')
            sympy_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', sympy_str)
            sympy_str = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', sympy_str)
            sympy_str = re.sub(r'\)([a-zA-Z])', r')*\1', sympy_str)
            sympy_str = re.sub(r'([a-zA-Z])\(', r'\1*(', sympy_str)
            
            # Handle exponential function
            sympy_str = re.sub(r'e\^\((.*?)\)', r'exp(\1)', sympy_str)
            sympy_str = re.sub(r'e\^(.*?)(?=[+\-*/) ]|$)', r'exp(\1)', sympy_str)
            
            expr = sp.sympify(sympy_str)
            original_latex = sp.latex(expr)
            
            # Get derivative and integral LaTeX
            derivative_expr = sp.diff(expr, x)
            integral_expr = sp.integrate(expr, x)
            
            # Simplify the expressions
            derivative_expr = sp.simplify(derivative_expr)
            integral_expr = sp.simplify(integral_expr)
            
            # Handle piecewise integrals
            if isinstance(integral_expr, sp.Piecewise):
                # Extract the main case from the piecewise
                main_case = integral_expr.args[0][0]
                # Simplify the main case
                main_case = sp.simplify(main_case)
                # Replace the piecewise with the simplified main case
                integral_expr = main_case
            
            # Handle exponential integrals specially
            if 'exp' in str(integral_expr):
                # For e^(kx), the integral is (1/k)e^(kx)
                integral_expr = sp.simplify(integral_expr)
            
            derivative_latex = sp.latex(derivative_expr)
            integral_latex = sp.latex(integral_expr)
            
            # Convert LaTeX to more readable format
            derivative_str = str(derivative_expr)
            integral_str = str(integral_expr)
            
            # Clean up the expressions
            derivative_str = derivative_str.replace('**', '^')
            derivative_str = derivative_str.replace('*', '')
            derivative_str = derivative_str.replace('exp', 'e^')
            derivative_str = derivative_str.replace('log(e)', '1')  # Simplify log(e) terms
            
            integral_str = integral_str.replace('**', '^')
            integral_str = integral_str.replace('*', '')
            integral_str = integral_str.replace('exp', 'e^')
            integral_str = integral_str.replace('log(e)', '1')  # Simplify log(e) terms
            
            # Update the derivative text field
            entry_2.delete("1.0", "end")
            entry_2.insert("1.0", f"d/dx({func_str}) = {derivative_str}")
            
            # Update the integral text field
            entry_3.delete("1.0", "end")
            entry_3.insert("1.0", f"∫({func_str})dx = {integral_str} + C")
            
            # Calculate definite integral if bounds are specified
            if integration_bounds:
                try:
                    definite_integral, _ = integrate.quad(func, integration_bounds[0], integration_bounds[1])
                    entry_3.insert("end", f"\n∫({func_str})dx from {integration_bounds[0]} to {integration_bounds[1]} = {definite_integral:.6f}")
                except:
                    pass
        except:
            # Fallback to simple text if LaTeX conversion fails
            original_latex = func_str
            derivative_latex = "f'(x)"
            integral_latex = "∫f(x)dx"
        
        # Calculate optimal x-range for original function
        y_values = np.array(y_values)
        y_range = max(y_values) - min(y_values)
        if y_range < 10:  # For functions with small range
            x_min_f, x_max_f = -5, 5
        else:  # For functions with larger range, find interesting region
            interesting_points = np.where(abs(y_values) <= max(abs(y_values)) * 2)[0]
            if len(interesting_points) > 0:
                x_min_f = max(-10, x_values[interesting_points[0]] - 1)
                x_max_f = min(10, x_values[interesting_points[-1]] + 1)
            else:
                x_min_f, x_max_f = -5, 5

        # Calculate optimal y-range for original function
        y_min_f = min(y_values) - y_range * 0.1
        y_max_f = max(y_values) + y_range * 0.1

        # Calculate derivative values and its optimal ranges
        if "d/dx" in derivative_text and "=" in derivative_text:
            derivative_expr = derivative_text.split("=")[1].strip()
            try:
                derivative_func = parse_user_function(derivative_expr)
                y_prime = [derivative_func(x_val) for x_val in x_values]
            except:
                y_prime = np.array([numerical_derivative(func, xi) for xi in x_values])
        else:
            y_prime = np.array([numerical_derivative(func, xi) for xi in x_values])

        # Calculate optimal ranges for derivative
        y_prime = np.array(y_prime)
        y_prime_range = max(y_prime) - min(y_prime)
        y_prime_min = min(y_prime) - y_prime_range * 0.1
        y_prime_max = max(y_prime) + y_prime_range * 0.1

        # Find interesting region for derivative
        if y_prime_range < 10:
            x_min_d, x_max_d = -5, 5
        else:
            interesting_points = np.where(abs(y_prime) <= max(abs(y_prime)) * 2)[0]
            if len(interesting_points) > 0:
                x_min_d = max(-10, x_values[interesting_points[0]] - 1)
                x_max_d = min(10, x_values[interesting_points[-1]] + 1)
            else:
                x_min_d, x_max_d = -5, 5

        # Calculate integral values and its optimal ranges
        try:
            if integral_expr:
                integral_func = parse_user_function(integral_expr)
                y_integral = [integral_func(x_val) for x_val in x_values]
            else:
                y_integral = np.zeros_like(x_values)
                for i in range(1, len(x_values)):
                    y_integral[i], _ = integrate.quad(func, x_min, x_values[i])
        except:
            y_integral = np.zeros_like(x_values)
            for i in range(1, len(x_values)):
                y_integral[i], _ = integrate.quad(func, x_min, x_values[i])

        # Calculate optimal ranges for integral
        y_integral = np.array(y_integral)
        y_integral_range = max(y_integral) - min(y_integral)
        y_integral_min = min(y_integral) - y_integral_range * 0.1
        y_integral_max = max(y_integral) + y_integral_range * 0.1

        # Find interesting region for integral
        if y_integral_range < 10:
            x_min_i, x_max_i = -5, 5
        else:
            interesting_points = np.where(abs(y_integral) <= max(abs(y_integral)) * 2)[0]
            if len(interesting_points) > 0:
                x_min_i = max(-10, x_values[interesting_points[0]] - 1)
                x_max_i = min(10, x_values[interesting_points[-1]] + 1)
            else:
                x_min_i, x_max_i = -5, 5

        # Update the graphs
        # Original function
        ax1.clear()
        ax1.set_facecolor("#3159EE")
        ax1.grid(True, linestyle='--', alpha=0.7, color='white')
        ax1.axhline(y=0, color='white', linestyle='-', alpha=0.3)
        ax1.axvline(x=0, color='white', linestyle='-', alpha=0.3)
        ax1.set_title('Original Function', fontsize=10, color='white')
        ax1.set_xlabel('x', fontsize=8, color='white')
        ax1.set_ylabel('f(x)', fontsize=8, color='white')
        ax1.tick_params(colors='white')
        ax1.spines['top'].set_color('white')
        ax1.spines['right'].set_color('white')
        ax1.spines['bottom'].set_color('white')
        ax1.spines['left'].set_color('white')
        
        # Set adaptive ranges for original function
        ax1.set_xlim(x_min_f, x_max_f)
        ax1.set_ylim(y_min_f, y_max_f)
        
        # Plot the function
        ax1.plot(x_values, y_values, color='#FFAB4C', linewidth=2)
        
        # If we have valid integration bounds, add vertical lines
        if integration_bounds:
            ax1.axvline(x=integration_bounds[0], color='white', linestyle='--', alpha=0.8)
            ax1.axvline(x=integration_bounds[1], color='white', linestyle='--', alpha=0.8)
            if definite_integral is not None:
                ax1.text(0.05, 0.05, f'Area = {definite_integral:.4f}', 
                         transform=ax1.transAxes, fontsize=9, color='white',
                         verticalalignment='bottom', bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
        
        # Add function expression as text
        ax1.text(0.05, 0.95, f'$f(x) = {original_latex}$', 
                 transform=ax1.transAxes, fontsize=9, color='white',
                 verticalalignment='top', bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
        
        canvas1.draw()
        
        # Derivative
        ax2.clear()
        ax2.set_facecolor("#3159EE")
        ax2.grid(True, linestyle='--', alpha=0.7, color='white')
        ax2.axhline(y=0, color='white', linestyle='-', alpha=0.3)
        ax2.axvline(x=0, color='white', linestyle='-', alpha=0.3)
        ax2.set_title('First Derivative', fontsize=10, color='white')
        ax2.set_xlabel('x', fontsize=8, color='white')
        ax2.set_ylabel('f\'(x)', fontsize=8, color='white')
        ax2.tick_params(colors='white')
        ax2.spines['top'].set_color('white')
        ax2.spines['right'].set_color('white')
        ax2.spines['bottom'].set_color('white')
        ax2.spines['left'].set_color('white')
        
        # Set adaptive ranges for derivative
        ax2.set_xlim(x_min_d, x_max_d)
        ax2.set_ylim(y_prime_min, y_prime_max)
        
        ax2.plot(x_values, y_prime, color='#69F5FF', linewidth=2)
        
        # Add derivative expression as text
        ax2.text(0.05, 0.95, f'$f\'(x) = {derivative_latex}$', 
                 transform=ax2.transAxes, fontsize=9, color='white',
                 verticalalignment='top', bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
        
        canvas2.draw()
        
        # Integral
        ax3.clear()
        ax3.set_facecolor("#3159EE")
        ax3.grid(True, linestyle='--', alpha=0.7, color='white')
        ax3.axhline(y=0, color='white', linestyle='-', alpha=0.3)
        ax3.axvline(x=0, color='white', linestyle='-', alpha=0.3)
        ax3.set_title('Integral', fontsize=10, color='white')
        ax3.set_xlabel('x', fontsize=8, color='white')
        ax3.set_ylabel('∫f(x)dx', fontsize=8, color='white')
        ax3.tick_params(colors='white')
        ax3.spines['top'].set_color('white')
        ax3.spines['right'].set_color('white')
        ax3.spines['bottom'].set_color('white')
        ax3.spines['left'].set_color('white')
        
        # Set adaptive ranges for integral
        ax3.set_xlim(x_min_i, x_max_i)
        ax3.set_ylim(y_integral_min, y_integral_max)
        
        # Plot the integral curve
        ax3.plot(x_values, y_integral, color='#69FF8A', linewidth=2)
        
        # If we have valid integration bounds, add vertical lines
        if integration_bounds:
            ax3.axvline(x=integration_bounds[0], color='white', linestyle='--', alpha=0.8)
            ax3.axvline(x=integration_bounds[1], color='white', linestyle='--', alpha=0.8)
            if definite_integral is not None:
                ax3.text(0.05, 0.05, f'Area = {definite_integral:.4f}', 
                         transform=ax3.transAxes, fontsize=9, color='white',
                         verticalalignment='bottom', bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
        
        # Add integral expression as text
        ax3.text(0.05, 0.95, f'$\\int f(x)dx = {integral_latex}$', 
                 transform=ax3.transAxes, fontsize=9, color='white',
                 verticalalignment='top', bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
        
        canvas3.draw()
        
    except Exception as e:
        print(f"Error updating graphs: {str(e)}")

# Initialize graphs with sample function
update_graphs("x^2 + 2x + 1")

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    311.0,
    736.0,
    image=image_image_8
)

#Graph for Original Function Location
image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    726.0,
    736.0,
    image=image_image_9
)

#Graph for First Derivative Location
image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    1132.0,
    736.0,
    image=image_image_10
)

#Graph for Numerical Integration Location
image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    1078.0,
    477.0,
    image=image_image_11
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    1079.0,
    477.0,
    image=entry_image_4
)

#LowerLimitEntry
entry_4 = Entry(
    bd=0,
    bg="#F3F3F3",
    fg=TEXT_COLOR,
    highlightthickness=0
)
entry_4.place(
    x=1030.0,
    y=461.0,
    width=98.0,
    height=30.0
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    1248.0,
    477.0,
    image=image_image_12
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    1248.0,
    477.0,
    image=entry_image_5
)

#UpperLimitEntry
entry_5 = Entry(
    bd=0,
    bg="#F3F3F3",
    fg=TEXT_COLOR,
    highlightthickness=0
)
entry_5.place(
    x=1199.0,
    y=461.0,
    width=98.0,
    height=30.0
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    668.0,
    303.0,
    image=image_image_13
)

image_image_14 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(
    312.0,
    425.0,
    image=image_image_14
)

image_image_15 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(
    202.0,
    556.0,
    image=image_image_15
)

image_image_16 = PhotoImage(
    file=relative_to_assets("image_16.png"))
image_16 = canvas.create_image(
    651.0,
    556.0,
    image=image_image_16
)

image_image_17 = PhotoImage(
    file=relative_to_assets("image_17.png"))
image_17 = canvas.create_image(
    1044.0,
    556.0,
    image=image_image_17
)

image_image_18 = PhotoImage(
    file=relative_to_assets("image_18.png"))
image_18 = canvas.create_image(
    704.0,
    425.0,
    image=image_image_18
)

image_image_19 = PhotoImage(
    file=relative_to_assets("image_19.png"))
image_19 = canvas.create_image(
    1108.0,
    425.0,
    image=image_image_19
)

image_image_20 = PhotoImage(
    file=relative_to_assets("image_20.png"))
image_20 = canvas.create_image(
    999.0,
    484.0,
    image=image_image_20
)

image_image_21 = PhotoImage(
    file=relative_to_assets("image_21.png"))
image_21 = canvas.create_image(
    1169.0,
    484.0,
    image=image_image_21
)

# Function to calculate the first derivative
def calculate_derivative():
    # Get the function from the input field
    func_str = entry_1.get()
    
    # Check if the function is empty or still has the placeholder
    if func_str == "" or func_str == "Enter your function here":
        entry_2.delete("1.0", "end")
        entry_2.insert("1.0", "Please enter a function")
        entry_2.config(fg=TEXT_COLOR)  # Set text color
        return
    
    try:
        # Parse the function using our enhanced parser
        func = parse_user_function(func_str)
        
        # Convert the function string to sympy format for derivative calculation
        x = sp.Symbol('x')
        sympy_str = func_str.replace('^', '**')
        sympy_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', sympy_str)
        sympy_str = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', sympy_str)
        sympy_str = re.sub(r'\)([a-zA-Z])', r')*\1', sympy_str)
        sympy_str = re.sub(r'([a-zA-Z])\(', r'\1*(', sympy_str)
        expr = sp.sympify(sympy_str)
        
        # Calculate the first derivative
        derivative = sp.diff(expr, x)
        
        # Convert the derivative to a more natural format
        derivative_str = str(derivative)
        derivative_str = derivative_str.replace('**', '^')
        derivative_str = derivative_str.replace('*', '')
        
        # Display the result
        entry_2.delete("1.0", "end")
        entry_2.insert("1.0", f"d/dx({func_str}) = {derivative_str}")
        entry_2.config(fg=TEXT_COLOR)  # Set text color
        
    except Exception as e:
        # If parsing fails, display error
        entry_2.delete("1.0", "end")
        entry_2.insert("1.0", f"Error: {str(e)}")
        entry_2.config(fg=TEXT_COLOR)  # Set text color

# Function to calculate the integral
def calculate_integral():
    # Get the function from the input field
    func_str = entry_1.get()
    
    # Check if the function is empty or still has the placeholder
    if func_str == "" or func_str == "Enter your function here":
        entry_3.delete("1.0", "end")
        entry_3.insert("1.0", "Please enter a function")
        entry_3.config(fg=TEXT_COLOR)  # Set text color
        return
    
    # Get the lower and upper limits
    try:
        lower_limit = float(entry_4.get())
        upper_limit = float(entry_5.get())
    except ValueError:
        entry_3.delete("1.0", "end")
        entry_3.insert("1.0", "Please enter valid limits")
        entry_3.config(fg=TEXT_COLOR)  # Set text color
        return
    
    try:
        # Parse the function using our enhanced parser
        func = parse_user_function(func_str)
        
        # Convert the function string to sympy format for integral calculation
        x = sp.Symbol('x')
        sympy_str = func_str.replace('^', '**')
        sympy_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', sympy_str)
        sympy_str = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', sympy_str)
        sympy_str = re.sub(r'\)([a-zA-Z])', r')*\1', sympy_str)
        sympy_str = re.sub(r'([a-zA-Z])\(', r'\1*(', sympy_str)
        expr = sp.sympify(sympy_str)
        
        # Calculate the indefinite integral
        indefinite_integral = sp.integrate(expr, x)
        
        # Calculate the definite integral
        definite_integral = sp.integrate(expr, (x, lower_limit, upper_limit))
        
        # Convert the integrals to a more natural format
        indefinite_str = str(indefinite_integral)
        indefinite_str = indefinite_str.replace('**', '^')
        indefinite_str = indefinite_str.replace('*', '')
        
        # Display the results
        entry_3.delete("1.0", "end")
        entry_3.insert("1.0", f"∫({func_str})dx = {indefinite_str} + C")
        entry_3.insert("end", f"\n∫({func_str})dx from {lower_limit} to {upper_limit} = {definite_integral}")
        entry_3.config(fg=TEXT_COLOR)  # Set text color
        
    except Exception as e:
        # If sympy fails, fall back to numerical integration
        result = process_user_integration(func_str, lower_limit, upper_limit)
        
        # Display the result
        entry_3.delete("1.0", "end")
        if result["success"]:
            entry_3.insert("1.0", f"Numerical result: {result['result']:.6f}")
        else:
            entry_3.insert("1.0", f"Error: {result['message']}")
        entry_3.config(fg=TEXT_COLOR)  # Set text color

# Function to calculate both derivative and integral
def calculate_all():
    # Get the function from the input field
    func_str = entry_1.get()
    
    # Calculate derivative and integral
    calculate_derivative()
    calculate_integral()
    
    # Update the graphs
    update_graphs(func_str)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=calculate_all,
    relief="flat"
)
button_1.place(
    x=877.0,
    y=334.0,
    width=98.0,
    height=42.0
)

button_image_hover_1 = PhotoImage(
    file=relative_to_assets("button_hover_1.png"))

def button_1_hover(e):
    button_1.config(
        image=button_image_hover_1
    )
def button_1_leave(e):
    button_1.config(
        image=button_image_1
    )

button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)

# Function to save graph as image
def save_graph_as_image(fig, default_filename):
    """Save the matplotlib figure as an image file with user-selected location"""
    try:
        # Ask user where to save the file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=default_filename,
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        # If user cancels the dialog, return False
        if not file_path:
            return False
        
        # Create a temporary file with the specified name
        fig.savefig(file_path, dpi=300, bbox_inches='tight', facecolor="#3159EE", edgecolor='white')
        return True, file_path
    except Exception as e:
        print(f"Error saving graph: {str(e)}")
        return False, None

# Function to save original function graph
def save_original_function_graph():
    """Save the original function graph as an image"""
    # Generate a filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"original_function_{timestamp}.png"
    
    # Save the graph
    success, file_path = save_graph_as_image(fig1, default_filename)
    if success:
        # Show success message
        messagebox.showinfo("Success", f"Graph saved as {file_path}")
    else:
        # Show error message only if user didn't cancel
        if file_path is None:
            messagebox.showerror("Error", "Failed to save graph")

# Function to save derivative graph
def save_derivative_graph():
    """Save the derivative graph as an image"""
    # Generate a filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"derivative_{timestamp}.png"
    
    # Save the graph
    success, file_path = save_graph_as_image(fig2, default_filename)
    if success:
        # Show success message
        messagebox.showinfo("Success", f"Graph saved as {file_path}")
    else:
        # Show error message only if user didn't cancel
        if file_path is None:
            messagebox.showerror("Error", "Failed to save graph")

# Function to save integral graph
def save_integral_graph():
    """Save the integral graph as an image"""
    # Generate a filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"integral_{timestamp}.png"
    
    # Save the graph
    success, file_path = save_graph_as_image(fig3, default_filename)
    if success:
        # Show success message
        messagebox.showinfo("Success", f"Graph saved as {file_path}")
    else:
        # Show error message only if user didn't cancel
        if file_path is None:
            messagebox.showerror("Error", "Failed to save graph")

#Save Graph for Original Function
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=save_original_function_graph,
    relief="flat"
)
button_4.place(
    x=122.0,
    y=903.0,
    width=156.0,
    height=34.0
)

button_image_hover_4 = PhotoImage(
    file=relative_to_assets("button_hover_4.png"))

def button_4_hover(e):
    button_4.config(
        image=button_image_hover_4
    )
def button_4_leave(e):
    button_4.config(
        image=button_image_4
    )

button_4.bind('<Enter>', button_4_hover)
button_4.bind('<Leave>', button_4_leave)

#Save Graph for Differentiation
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=save_derivative_graph,
    relief="flat"
)
button_2.place(
    x=536.0,
    y=903.0,
    width=156.0,
    height=34.0
)

button_image_hover_2 = PhotoImage(
    file=relative_to_assets("button_hover_2.png"))

def button_2_hover(e):
    button_2.config(
        image=button_image_hover_2
    )
def button_2_leave(e):
    button_2.config(
        image=button_image_2
    )

button_2.bind('<Enter>', button_2_hover)
button_2.bind('<Leave>', button_2_leave)

#Save Graph for Integration
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=save_integral_graph,
    relief="flat"
)
button_3.place(
    x=942.0,
    y=903.0,
    width=156.0,
    height=34.0
)

button_image_hover_3 = PhotoImage(
    file=relative_to_assets("button_hover_3.png"))

def button_3_hover(e):
    button_3.config(
        image=button_image_hover_3
    )
def button_3_leave(e):
    button_3.config(
        image=button_image_3
    )

button_3.bind('<Enter>', button_3_hover)
button_3.bind('<Leave>', button_3_leave)

# After all your Entry and Text widgets are created:
add_placeholder(entry_1, "e.g. x^2 + 2x + 1")
add_placeholder(entry_2, "e.g. d/dx(x^2 + 2x + 1) = 2x + 2", is_entry=False)
add_placeholder(entry_3, "e.g. ∫(x^2 + 2x + 1)dx = x^3/3 + x^2 + x + C", is_entry=False)
add_placeholder(entry_4, "Lower bound (e.g. 0)")
add_placeholder(entry_5, "Upper bound (e.g. 2)")

window.resizable(False, False)
window.mainloop()
