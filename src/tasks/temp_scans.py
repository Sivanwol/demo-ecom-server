import os
import shutil

from config.containers import celery, app


@celery.task()
def clear_temp_unhandled_files(a, b):
    # let clear temp folder
    upload_temp_path = os.path.join(app.flask_app.config.UPLOAD_FOLDER,
                                    app.flask_app.config.UPLOAD_TEMP_FOLDER)
    for filename in os.listdir(upload_temp_path):
        file_path = os.path.join(upload_temp_path, filename)
        if file_path != os.path.join(upload_temp_path, '.gitkeep'):
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
