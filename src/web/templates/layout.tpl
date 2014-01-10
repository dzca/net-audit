<!doctype html>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>Enterprise Security Monitor</title>
        <link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">
        <script type="text/javascript" src="http://code.jquery.com/jquery-latest.js">
        </script>
        <script>
           $(document).ready(function() {
               $('#hours-table tr:even').css('background-color','#dddddd');
            });
        </script>
    </head>
    <body>
        <div id="wrapper">
            <div id="header">
                <div class="navigation">
                    <ul>
                        <li><a href="/event">Event</a></li>
                        <li><a href="/stat">Statistics</a></li>
                        <li><a href="/monthly">Monthly Report</a></li>
                        <li><a href="/help">Help</a></li>
                        <li><a href="/logout">Log out</a></li>
                    </ul>
                </div>
            </div>
            <div id="content">
            {% block body %}{% endblock %}
            </div>
            <div id="footer">
                    <div id="legal">Copyright &copy; 2009-2012 vollov.ca All Rights Reserved. Designed by: vollov.ca [at] gmail.com.</div>
            </div>
        <div>
        <!--end of wrapper-->
    </body>
</html>