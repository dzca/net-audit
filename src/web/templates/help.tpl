{% extends "layout.tpl" %}
{% block body %}
    <div id='help'>
        <h3>How to write query</h3>
        <ul>
            <li>events in a day: create_time in 2012-12-13</li>
            <li>events in a month: create_time in 2012-12</li>
            <li>events in a time range: create_time >2012-11-25T21:49:00Z and create_time <= 2012-11-25T21:49:13Z</li>
            <li>query with like: domain like 'twitter.com'</li>
            <li>query in : ip in (19.2.13.4, 19.3.24.56)</li>
            <li>query with and: ip = 10.30.13.11 and domain = 'www.cnn.com'</li>
            <li>query size: size >= 1000 </li>        
        </ul>
        <h3>Supported operators</h3>
        >, <, >=, <=, like, in(a,b,c),=, != 
    </div>
{% endblock %}