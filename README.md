## `async_assignment`

The `async_assignment` module simplifies asynchronous task execution in PySide2 applications by offloading long-running tasks to a separate thread while keeping the main UI responsive.

### Features
- **Asynchronous Execution**: Tasks (`working`) run in a separate QThread, preventing the UI from freezing.
- **UI-Safe Callbacks**: Ensures that `callback` functions run in the main thread, allowing safe UI updates.
- **Support for Parameters**: Pass positional (`args`) and keyword arguments (`kwargs`) to the `working` function.
- **Automatic Thread Management**: Manages the lifecycle of QThread and Worker objects automatically.

### How It Works
1. **Define a task (`working`)**:
   - A long-running function you want to run in a separate thread.
2. **Define a callback (`callback`)**:
   - A function to update the UI or perform other tasks after the work is done.
3. **Use `async_assignment`**:
   - Create an instance of `async_assignment` with `working` and `callback`.
   - Call `start_async()` to begin the task.
   
### Installation
Ensure you have **PySide2** installed:
```bash
pip install PySide2
```
Example: Integration with PySide2 UI
Minimal Example:
```python
...
self.button = QtWidgets.QPushButton("Start Working Async")
self.async_assignment = async_assignment( working = self.working,
                                          callback = self.on_work_done)
self.button.clicked.connect(self.async_assignment.start_async)
...

def working(self):
    result = sum(range(1, 1001))  # Add numbers from 1 to 1000
    time.sleep(3)  # Simulate long task
    self.result = result
    print(f"Sum result: {result}")

def on_work_done(self):
    self.textbox.setText(str(self.result))
```

### Advanced Features:
### Passing Parameters to working:
1. **Passing Parameters to `working`:**
```python
worker = async_assignment(
    working=long_task,
    callback=update_ui,
    args=[param1, param2],
    kwargs={'key': 'value'}
)
```
2. **Customizing UI Components:**
    - Combine with PySide2 widgets for advanced workflows.