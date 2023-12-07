# mimic_user_agent

Funcion que retorna un 'user-agent' falso aleatorio o estático.

# Uso

```python
>>> from mimic_useragent import mimic_user_agent
>>> mimic_user_agent()
'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
>>>
>>> mimic_user_agent(seed=10)
'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0'
```

Recibe un parámetro `int` para el uso de una *seed*, por defecto es `None`.

---

**Aclaración:**

Por ahora, solamente genera user-agent Firefox.

---

# Tests

```python
python -m unittest
```
