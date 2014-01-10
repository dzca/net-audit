{% extends "layout.tpl" %}
{% block body %}
    <div id='query'>
        <form method="POST" action='/stat'>
            <input id="txtQuery" name="stat_query" size=50 type="text" />
            <input id="btnQuerySubmit" type="submit" value="Search" />
        </form>
        <br>
        {% if time %}
    	<h3>Report of {{ time }}</h3>
    	{% endif %}
	    <table id='result-table'>
	      <tr>
	        <th>Source IP</th>
	        <th>Total downloads (bytes)</th>
	      </tr>
	    {% for stat in stats %}
			<tr class="{{ loop.cycle('odd', 'even') }}">
			    <td>{{ stat.ip }}</td>
			    <td>{{ stat.size }}</td>
			</tr>
	    {% endfor %}
	    
    	</table>
    </div>
{% endblock %}