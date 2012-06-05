<!doctype html>
<html>


<head>
  <meta charset="utf-8">
  <title>Trivial Trunk</title>
</head>


<body>

<p>Every time this page is loaded, an interaction record is created.</p>
<p>If you click on the following link you will go to another site.</p>
<p>That site will confirm that you completed the interaction, giving you a score of one.</p>
<p><a href="http://trivial-leaf.appspot.com/?d=http://trivial-trunk.appspot.com/&i={{ i }}">Complete your interaction</a></p>
<ul>
{% for interaction in interactions %}
 <li>
 Interaction created: {{ interaction.date }},
 {% if interaction.score %}
  has score: {{ interaction.score }}
 {% else %}
  has no score
 {% endif %}
 </li>
{% endfor %}
</ul>

<a href="https://github.com/ajschumacher/trivial-trunk"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png" alt="Fork me on GitHub"></a>

</body>


</html>
