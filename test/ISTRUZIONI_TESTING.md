Requisiti per avviare i test:
  <ul>
    <li>Browser web Chrome (versione minima 81)</li>
    <li>Pacchetto selenium installato </li>
  <ul><br>

Se selenium non è presente digitare da terminale il comando: <code>pip install selenium</code><br><br>


Per avviare gli unit test relativi alle singole app immettere da terminale, nella cartella principale del progetto AnalizzailVocabolario, il comando:<br>
<code>python manage.py test [nome_app]</code> <br>
Dove nome_app è un argormento tra:
<ul>
  <li>accounts\tests</li>
  <li>AV\tests</li>
  <li>catalogo\tests</li>
  <li>Text_manipulation\tests</li>
</ul>

Per avviare gli integration test immettere da terminale, nella cartella principale del progetto AnalizzailVocabolario, il comando:<br>
<code>python manage.py test integration_test</code> <br>

E' inoltre possibile avviare tutti i test immettendo da terminale, nella cartella principale del progetto AnalizzailVocabolario, il comando: <br>
<code>python manage.py test</code> <br>
