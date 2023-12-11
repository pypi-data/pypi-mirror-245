# Hojo - An Opinionated ORM on Top of SQL Alchemy

Hojo is a library that simplifies the usage of SQL Alchemy, providing an interface that is familiar to Django users. While it is not an exact replication of the Django ORM API, it strives to be reminiscent of it, making it easier for Django developers to work with SQL Alchemy.

**Please note that this library is currently in Alpha version and is not yet ready for production use.**

## Installation

You can install Hojo using pip:

```bash
pip install hojo
```

## Basic Usage
Here's a basic example of how to use Hojo:


```python
from hojo import BaseModel, dataclass

@dataclass
class Soldier(BaseModel):
    name: str
    weapon: str

# Create a Soldier instance
hero = Soldier(name='Cloud', weapon='Buster Sword') 

# Insert the hero into the 'soldiers' table
Soldier.objects.create(hero)

# Retrieve a Soldier with the name 'Cloud' from the 'soldiers' table
cloud = Soldier.objects.filter(name='Cloud')

```
    