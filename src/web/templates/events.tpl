{% extends "layout.tpl" %}
{% block body %}
    <div id='query'>
        <form method="POST" action='/event'>
            <input id="txtQuery" name="event_query" size=50 type="text" />
            <input id="btnQuerySubmit" type="submit" value="Search" />
        </form>
        <br>
    
        <table id='result-table'>
          <tr>
            <th>ID</th>
            <th>Connect Time</th>
            <th>Domain</th>
            <th>Source IP</th>
            <th>Download Size(bytes)</th>
          </tr>
          
        {% for event in events %}
          <tr class="{{ loop.cycle('odd', 'even') }}">
            <td>{{ event.index }}</td>
            <td>{{ event.time }}</td>
            <td>{{ event.domain }}</td>
            <td>{{ event.ip }}</td>
            <td>{{ event.size }}</td>
          </tr>
        {% endfor %}
        </table>
        
        <div class='navigation'>
            <ul>
                {% if pager.previous == 0 %}
                    <li>Previous Page</li>
                {% else %}
                    <li><a href='/event/{{ pager.previous }}'>Previous Page</a></li>
                {% endif %}
                    <li> {{ pager.current }} / {{ pager.pages }} </li>
                {% if pager.next == 0 %}
                    <li>Next Page</li>
                {% else %}
                    <li><a href='/event/{{ pager.next }}'>Next Page</a></li>
                {% endif %}
            </ul>
        </div>
    </div>
{% endblock %}