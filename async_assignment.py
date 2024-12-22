from PySide2.QtCore import QObject, QThread, Signal

class Worker(QObject):
    """
    Worker class that encapsulates a task to be run asynchronously in a QThread.
    It emits signals when the task is finished or when a callback needs to be executed.
    """
    finished = Signal()  # Signal emitted when the task is finished
    call_main_callback = Signal()  # Signal emitted to execute the callback in the main thread

    def __init__(self, working=None, callback=None, args=None, kwargs=None):
        """
        Initialize the Worker with the task, callback, and optional arguments.

        :param working: Function to execute asynchronously.
        :param callback: Function to execute after the working function is complete.
        :param args: Positional arguments for the working function.
        :param kwargs: Keyword arguments for the working function.
        """
        super().__init__()
        self.working = working
        self.callback = callback
        self.args = args if args else []
        self.kwargs = kwargs if kwargs else {}

    def run(self):
        """
        Execute the working function with the provided arguments.
        """
        print('Running working function...')
        try:
            if self.working:
                self.working(*self.args, **self.kwargs)  # Pass args and kwargs to working
            if self.callback:
                print('Emitting callback signal...')
                self.call_main_callback.emit()  # Notify main thread to run the callback
        finally:
            self.finished.emit()  # Notify that the task is completed


class async_assignment(QObject):
    """
    A helper class to execute tasks asynchronously with minimal setup.
    It manages QThread and Worker objects, ensuring the task and callback run correctly.
    """

    def __init__(self, working=None, callback=None, args=None, kwargs=None):
        """
        Initialize async_assignment with a task, callback, and optional arguments.

        :param working: Function to execute asynchronously.
        :param callback: Function to execute after the working function is complete.
        :param args: Positional arguments for the working function.
        :param kwargs: Keyword arguments for the working function.
        """
        super().__init__()
        print('init async assignment')
        self.working = working
        self.callback = callback
        self.args = args if args else []
        self.kwargs = kwargs if kwargs else {}

    def start_async(self):
        """
        Start the asynchronous task with optional arguments.
        """
        print('Starting async work...')
        if not self.working:
            raise ValueError("You must define a working function.")

        # Create QThread and Worker
        self.thread = QThread()
        self.worker = Worker(working=self.working, callback=self.callback, args=self.args, kwargs=self.kwargs)
        self.worker.moveToThread(self.thread)

        # Connect signals
        self.worker.finished.connect(self._cleanup_thread)
        if self.callback:
            self.worker.call_main_callback.connect(self.callback)

        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)

        # Start the QThread
        self.thread.start()

    def _cleanup_thread(self):
        """
        Cleanup the QThread and Worker after the task is finished.
        """
        print("Cleaning up thread...")
        self.worker.deleteLater()  # Delete the Worker object
        self.thread.quit()  # Stop the QThread
        self.thread.wait()  # Wait for the QThread to finish
        self.thread = None
        self.worker = None
