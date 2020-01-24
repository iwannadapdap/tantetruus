from flask import jsonify, blueprints, redirect, render_template


def return_json(success: bool, data: dict = None, error=None):
    return jsonify(
        {
            'success': success,
            'data': data,
            'error': error
        }
    )


def return_message(title, content, delay, url):
    return render_template('message.html',
                           title=title,
                           content=content,
                           r_time=str(delay),
                           r_url=url)
