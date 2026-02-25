# REPO BLUEPRINT: member

## 🛠 TECH STACK: Django

### 📦 DJANGO APPS
users, chat, bohr_corp, bohr_api, bohr_common

### 🏗 DATA MODELS
- **users**: Profile, UserEmail, UserSession
- **chat**: ChatUser, Room, Participant, Message

## 📂 DIRECTORY STRUCTURE (L2)
```
├── manage.py
├── README.md
├── ECHONET IoT MASTER登録申請申請書.xlsx
├── doc/
 
 
 
 
├
─
─
 
s
e
t
u
p


 
 
 
 
├
─
─
 
p
e
r
m
i
s
s
i
o
n
s
.
t
x
t


 
 
 
 
├
─
─
 
m
e
m
b
e
r
_
d
o
c
u
m
e
n
t
a
t
i
o
n
.
p
d
f
├── users/
 
 
 
 
├
─
─
 
m
i
g
r
a
t
i
o
n
s
/


 


 


 


 


 


 


 


 


├


─


─


 


0


0


0


1


_


i


n


i


t


i


a


l


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


_


_


i


n


i


t


_


_


.


p


y


 
 
 
 
├
─
─
 
a
p
p
s
.
p
y


 
 
 
 
├
─
─
 
_
_
i
n
i
t
_
_
.
p
y


 
 
 
 
├
─
─
 
a
d
m
i
n
.
p
y


 
 
 
 
├
─
─
 
v
i
e
w
s
.
p
y


 
 
 
 
├
─
─
 
m
o
d
e
l
s
.
p
y
├── setup.txt
├── -F6jfjtqLzI2JPCgQBnw7HFyzSD-AsregP8VFBEj75vY0rw-oME.pkl
├── chat/
 
 
 
 
├
─
─
 
m
i
g
r
a
t
i
o
n
s
/


 


 


 


 


 


 


 


 


├


─


─


 


0


0


0


1


_


i


n


i


t


i


a


l


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


_


_


i


n


i


t


_


_


.


p


y


 
 
 
 
├
─
─
 
t
e
s
t
s
.
p
y


 
 
 
 
├
─
─
 
a
p
p
s
.
p
y


 
 
 
 
├
─
─
 
u
r
l
s
.
p
y


 
 
 
 
├
─
─
 
t
e
m
p
l
a
t
e
s
/


 


 


 


 


 


 


 


 


├


─


─


 


c


h


a


t


/


 
 
 
 
├
─
─
 
_
_
i
n
i
t
_
_
.
p
y


 
 
 
 
├
─
─
 
u
t
i
l
s
.
p
y


 
 
 
 
├
─
─
 
a
d
m
i
n
.
p
y


 
 
 
 
├
─
─
 
v
i
e
w
s
.
p
y


 
 
 
 
├
─
─
 
m
o
d
e
l
s
.
p
y
├── formats/
 
 
 
 
├
─
─
 
e
n
/


 


 


 


 


 


 


 


 


├


─


─


 


f


o


r


m


a


t


s


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


_


_


i


n


i


t


_


_


.


p


y


 
 
 
 
├
─
─
 
_
_
i
n
i
t
_
_
.
p
y
├── get-pip.py
├── common/
 
 
 
 
├
─
─
 
a
p
p
s
/


 


 


 


 


 


 


 


 


├


─


─


 


d


i


g


i


t


a


l


_


t


e


x


t


/


 
 
 
 
├
─
─
 
t
e
m
p
l
a
t
e
s
/


 


 


 


 


 


 


 


 


├


─


─


 


d


i


g


i


t


a


l


_


t


e


x


t


/
├── migrate_db.py
├── bohr_corp/
 
 
 
 
├
─
─
 
v
i
e
w
s
_
i
n
s
t
.
p
y


 
 
 
 
├
─
─
 
m
i
g
r
a
t
i
o
n
s
/


 


 


 


 


 


 


 


 


├


─


─


 


_


_


i


n


i


t


_


_


.


p


y


 
 
 
 
├
─
─
 
v
i
e
w
s
_
s
t
u
d
e
n
t
.
p
y


 
 
 
 
├
─
─
 
p
r
o
c
e
s
s
e
s
.
p
y


 
 
 
 
├
─
─
 
a
p
p
s
.
p
y


 
 
 
 
├
─
─
 
f
u
n
c
t
i
o
n
s
_
i
n
s
t
.
p
y


 
 
 
 
├
─
─
 
h
e
l
p
e
r
s
.
p
y


 
 
 
 
├
─
─
 
s
e
r
i
a
l
i
z
e
r
s
_
r
e
n
e
w
a
l
.
p
y


 
 
 
 
├
─
─
 
u
r
l
s
.
p
y


 
 
 
 
├
─
─
 
c
o
n
s
t
a
n
t
s
.
p
y


 
 
 
 
├
─
─
 
f
u
n
c
t
i
o
n
s
_
s
t
u
d
e
n
t
.
p
y


 
 
 
 
├
─
─
 
f
u
n
c
t
i
o
n
s
_
a
d
m
i
n
.
p
y


 
 
 
 
├
─
─
 
v
i
e
w
s
_
a
d
m
i
n
.
p
y


 
 
 
 
├
─
─
 
w
a
t
c
h
_
h
i
s
t
o
r
y
_
m
i
g
r
a
t
i
o
n
.
p
y


 
 
 
 
├
─
─
 
f
u
n
c
t
i
o
n
s
_
c
o
m
m
o
n
.
p
y


 
 
 
 
├
─
─
 
v
i
e
w
s
_
c
o
m
m
o
n
.
p
y


 
 
 
 
├
─
─
 
_
_
i
n
i
t
_
_
.
p
y
├── requirements/
 
 
 
 
├
─
─
 
o
l
d
_
p
r
o
d
.
t
x
t


 
 
 
 
├
─
─
 
s
t
a
g
i
n
g
.
t
x
t


 
 
 
 
├
─
─
 
o
l
d
_
d
e
v
.
t
x
t


 
 
 
 
├
─
─
 
d
e
v
.
t
x
t


 
 
 
 
├
─
─
 
o
l
d
_
s
t
a
g
i
n
g
.
t
x
t


 
 
 
 
├
─
─
 
p
r
o
d
.
t
x
t
├── NotoSansJP-Regular.pkl
├── scripts.py
├── bohr_api/
 
 
 
 
├
─
─
 
m
i
g
r
a
t
i
o
n
s
/


 


 


 


 


 


 


 


 


├


─


─


 


_


_


i


n


i


t


_


_


.


p


y


 
 
 
 
├
─
─
 
q
u
e
r
y
_
d
e
b
u
g
g
e
r
.
p
y


 
 
 
 
├
─
─
 
f
u
n
c
t
i
o
n
s
.
p
y


 
 
 
 
├
─
─
 
a
p
p
s
.
p
y


 
 
 
 
├
─
─
 
s
e
r
i
a
l
i
z
e
r
s
.
p
y


 
 
 
 
├
─
─
 
u
r
l
s
.
p
y


 
 
 
 
├
─
─
 
_
_
i
n
i
t
_
_
.
p
y


 
 
 
 
├
─
─
 
u
t
i
l
s
.
p
y


 
 
 
 
├
─
─
 
e
m
a
i
l
/


 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


o


t


p


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


d


o


c


_


a


p


p


l


y


_


s


t


a


f


f


_


e


d


u


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


d


o


c


_


a


p


p


l


y


_


r


e


s


k


i


l


l


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


d


o


c


_


a


p


p


l


y


_


e


n


r


o


l


l


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


c


a


n


c


e


l


_


e


m


a


i


l


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


d


o


c


_


a


p


p


l


y


_


s


t


a


f


f


_


r


e


s


k


i


l


l


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


d


a


t


a


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


d


o


c


_


a


p


p


l


y


_


e


d


u


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


d


o


c


_


a


p


p


l


y


_


s


t


a


f


f


_


e


n


r


o


l


l


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


t


r


a


n


s


f


e


r


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


d


o


c


_


a


p


p


l


y


_


a


t


t


e


n


d


a


n


c


e


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


d


o


c


_


a


p


p


l


y


_


s


t


a


f


f


_


a


t


t


e


n


d


a


n


c


e


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


v


e


r


i


f


y


.


p


y


 
 
 
 
├
─
─
 
v
i
e
w
s
.
p
y


 
 
 
 
├
─
─
 
m
o
d
e
l
s
.
p
y
├── documentation_website/
 
 
 
 
├
─
─
 
u
r
l
s
.
p
y


 
 
 
 
├
─
─
 
_
_
i
n
i
t
_
_
.
p
y


 
 
 
 
├
─
─
 
v
i
e
w
s
.
p
y


 
 
 
 
├
─
─
 
i
n
i
t
.
p
y
├── kikuichimonji/
 
 
 
 
├
─
─
 
s
e
t
t
i
n
g
s
.
p
y


 
 
 
 
├
─
─
 
s
e
t
t
i
n
g
s
_
l
o
c
a
l
.
p
y


 
 
 
 
├
─
─
 
a
p
p
s
/


 


 


 


 


 


 


 


 


├


─


─


 


s


t


o


r


y


/






 


 


 


 


 


 


 


 


├


─


─


 


q


a


s


y


s


t


e


m


/






 


 


 


 


 


 


 


 


├


─


─


 


l


i


b


r


a


r


y


/






 


 


 


 


 


 


 


 


├


─


─


 


p


r


i


c


e


/






 


 


 


 


 


 


 


 


├


─


─


 


m


a


i


n


t


e


n


a


n


c


e


/






 


 


 


 


 


 


 


 


├


─


─


 


c


o


r


e


/






 


 


 


 


 


 


 


 


├


─


─


 


i


a


_


a


d


m


i


n


/






 


 


 


 


 


 


 


 


├


─


─


 


s


c


h


o


o


l


/






 


 


 


 


 


 


 


 


├


─


─


 


p


e


r


f


o


r


m


a


n


c


e


/






 


 


 


 


 


 


 


 


├


─


─


 


e


v


e


n


t


/






 


 


 


 


 


 


 


 


├


─


─


 


r


e


s


e


r


v


a


t


i


o


n


/






 


 


 


 


 


 


 


 


├


─


─


 


q


u


e


s


t


i


o


n


n


a


i


r


e


/






 


 


 


 


 


 


 


 


├


─


─


 


c


o


r


p


o


r


a


t


e


/






 


 


 


 


 


 


 


 


├


─


─


 


e


x


a


m


/






 


 


 


 


 


 


 


 


├


─


─


 


p


a


y


m


e


n


t


/






 


 


 


 


 


 


 


 


├


─


─


 


j


o


b


_


o


u


t


s


o


u


r


c


i


n


g


/






 


 


 


 


 


 


 


 


├


─


─


 


d


a


t


a


_


a


n


a


l


y


s


i


s


/






 


 


 


 


 


 


 


 


├


─


─


 


c


u


s


t


o


m


e


r


/






 


 


 


 


 


 


 


 


├


─


─


 


k


n


o


w


l


e


d


g


e


_


c


e


n


t


r


e


/






 


 


 


 


 


 


 


 


├


─


─


 


i


n


s


t


r


u


c


t


o


r


/






 


 


 


 


 


 


 


 


├


─


─


 


c


o


n


t


r


a


c


t


/






 


 


 


 


 


 


 


 


├


─


─


 


a


n


a


l


y


t


i


c


s


/






 


 


 


 


 


 


 


 


├


─


─


 


e


q


u


i


p


m


e


n


t


/






 


 


 


 


 


 


 


 


├


─


─


 


c


o


n


t


a


c


t


/






 


 


 


 


 


 


 


 


├


─


─


 


s


t


o


r


i


e


s


/






 


 


 


 


 


 


 


 


├


─


─


 


s


t


a


f


f


/






 


 


 


 


 


 


 


 


├


─


─


 


_


_


i


n


i


t


_


_


.


p


y


 
 
 
 
├
─
─
 
m
i
d
d
l
e
w
a
r
e
.
p
y


 
 
 
 
├
─
─
 
u
r
l
s
.
p
y


 
 
 
 
├
─
─
 
u
t
i
l
s
/


 


 


 


 


 


 


 


 


├


─


─


 


m


e


s


s


a


g


e


_


t


y


p


e


s


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


f


o


r


m


s


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


c


h


o


i


c


e


s


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


w


i


d


g


e


t


s


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


x


c


e


l


_


e


x


p


o


r


t


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


a


p


i


_


p


e


r


m


i


s


i


o


n


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


u


t


i


l


s


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


i


n


i


t


i


a


l


_


d


a


t


a


.


p


y


 
 
 
 
├
─
─
 
s
e
t
t
i
n
g
s
_
l
o
c
a
l
.
p
y
:
Z
o
n
e
.
I
d
e
n
t
i
f
i
e
r


 
 
 
 
├
─
─
 
t
e
s
t
.
p
y


 
 
 
 
├
─
─
 
w
s
g
i
.
p
y


 
 
 
 
├
─
─
 
t
e
m
p
l
a
t
e
s
/


 


 


 


 


 


 


 


 


├


─


─


 


s


t


o


r


y


/






 


 


 


 


 


 


 


 


├


─


─


 


a


d


m


i


n


_


b


a


s


e


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


q


a


s


y


s


t


e


m


/






 


 


 


 


 


 


 


 


├


─


─


 


s


u


b


_


n


a


v


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


l


i


b


r


a


r


y


/






 


 


 


 


 


 


 


 


├


─


─


 


p


r


i


c


e


/






 


 


 


 


 


 


 


 


├


─


─


 


m


a


i


n


t


e


n


a


n


c


e


/






 


 


 


 


 


 


 


 


├


─


─


 


e


m


p


t


y


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


c


o


r


e


/






 


 


 


 


 


 


 


 


├


─


─


 


i


a


_


a


d


m


i


n


/






 


 


 


 


 


 


 


 


├


─


─


 


s


u


b


_


n


a


v


_


c


o


r


p


_


t


r


a


i


n


i


n


g


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


s


c


h


o


o


l


/






 


 


 


 


 


 


 


 


├


─


─


 


p


e


r


f


o


r


m


a


n


c


e


/






 


 


 


 


 


 


 


 


├


─


─


 


d


a


t


e


_


r


a


n


g


e


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


e


v


e


n


t


/






 


 


 


 


 


 


 


 


├


─


─


 


r


e


s


e


r


v


a


t


i


o


n


/






 


 


 


 


 


 


 


 


├


─


─


 


q


u


e


s


t


i


o


n


n


a


i


r


e


/






 


 


 


 


 


 


 


 


├


─


─


 


p


a


g


i


n


a


t


i


o


n


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


c


o


r


p


o


r


a


t


e


/






 


 


 


 


 


 


 


 


├


─


─


 


e


x


a


m


/






 


 


 


 


 


 


 


 


├


─


─


 


m


e


s


s


a


g


e


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


4


0


4


_


e


r


r


o


r


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


p


a


y


m


e


n


t


/






 


 


 


 


 


 


 


 


├


─


─


 


j


o


b


_


o


u


t


s


o


u


r


c


i


n


g


/






 


 


 


 


 


 


 


 


├


─


─


 


c


u


s


t


o


m


e


r


/






 


 


 


 


 


 


 


 


├


─


─


 


r


e


g


i


s


t


r


a


t


i


o


n


/






 


 


 


 


 


 


 


 


├


─


─


 


s


u


b


_


n


a


v


_


c


o


r


p


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


n


a


v


b


a


r


s


/






 


 


 


 


 


 


 


 


├


─


─


 


k


n


o


w


l


e


d


g


e


_


c


e


n


t


r


e


/






 


 


 


 


 


 


 


 


├


─


─


 


i


n


s


t


r


u


c


t


o


r


/






 


 


 


 


 


 


 


 


├


─


─


 


c


o


n


t


r


a


c


t


/






 


 


 


 


 


 


 


 


├


─


─


 


a


n


a


l


y


t


i


c


s


/






 


 


 


 


 


 


 


 


├


─


─


 


s


u


b


_


n


a


v


_


m


a


i


n


t


e


n


a


n


c


e


_


m


o


d


i


f


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


e


q


u


i


p


m


e


n


t


/






 


 


 


 


 


 


 


 


├


─


─


 


c


o


n


t


a


c


t


/






 


 


 


 


 


 


 


 


├


─


─


 


s


t


o


r


i


e


s


/






 


 


 


 


 


 


 


 


├


─


─


 


s


u


b


_


n


a


v


_


a


p


p


l


i


c


a


t


i


o


n


s


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


s


t


a


f


f


/






 


 


 


 


 


 


 


 


├


─


─


 


b


a


s


e


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


s


u


b


_


n


a


v


_


j


o


b


_


o


u


t


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


p


a


g


i


n


a


t


i


o


n


2


.


h


t


m


l


 
 
 
 
├
─
─
 
_
_
i
n
i
t
_
_
.
p
y
├── coupon_calc_script.py
├── logs/
 
 
 
 
├
─
─
 
l
o
g
f
i
l
e
.
l
o
g


 
 
 
 
├
─
─
 
s
e
n
t
_
l
o
g
f
i
l
e
.
l
o
g
├── mem/
 
 
 
 
├
─
─
 
m
e
d
i
a
/


 


 


 


 


 


 


 


 


├


─


─


 


c


k


e


d


i


t


o


r


/






 


 


 


 


 


 


 


 


├


─


─


 


p


d


f


_


f


i


l


e


_


a


p


p


l


i


/






 


 


 


 


 


 


 


 


├


─


─


 


n


o


t


i


f


i


c


a


t


i


o


n


s


/






 


 


 


 


 


 


 


 


├


─


─


 


c


o


r


p


/
├── scripts/
 
 
 
 
├
─
─
 
m
e
m
b
e
r
_
m
e
r
g
e
_
m
i
g
r
a
t
e
.
s
h


 
 
 
 
├
─
─
 
d
o
c
u
m
e
n
t
a
t
i
o
n
_
r
e
l
o
a
d
.
s
h


 
 
 
 
├
─
─
 
m
a
k
e
_
d
b
_
b
a
c
k
u
p
.
s
h


 
 
 
 
├
─
─
 
a
d
d
_
c
a
t
c
h
u
p
_
p
l
a
y
l
i
s
t
_
t
y
p
e
.
p
y


 
 
 
 
├
─
─
 
m
a
c
o
s
_
r
e
s
t
o
r
e
_
d
b
_
b
a
c
k
u
p
.
s
h


 
 
 
 
├
─
─
 
c
o
u
r
s
e
_
m
o
d
e
l
_
m
i
g
r
a
t
i
o
n
s
.
p
y


 
 
 
 
├
─
─
 
r
e
s
t
o
r
e
_
d
b
_
b
a
c
k
u
p
.
s
h


 
 
 
 
├
─
─
 
t
e
s
t
_
s
e
r
v
e
r
_
r
e
s
t
o
r
e
_
d
b
_
f
r
o
m
_
b
a
c
k
u
p
.
s
h
├── NotoSansJP-VariableFont_wght.pkl
├── corp/
 
 
 
 
├
─
─
 
a
p
p
s
/


 


 


 


 


 


 


 


 


├


─


─


 


c


o


r


p


o


r


a


t


i


o


n


/


 
 
 
 
├
─
─
 
t
e
m
p
l
a
t
e
s
/


 


 


 


 


 


 


 


 


├


─


─


 


c


o


r


p


o


r


a


t


i


o


n


/
├── static/
 
 
 
 
├
─
─
 
f
u
l
l
c
a
l
e
n
d
a
r
-
5
.
4
.
0
/


 


 


 


 


 


 


 


 


├


─


─


 


R


E


A


D


M


E


.


m


d






 


 


 


 


 


 


 


 


├


─


─


 


L


I


C


E


N


S


E


.


t


x


t






 


 


 


 


 


 


 


 


├


─


─


 


e


x


a


m


p


l


e


s


/






 


 


 


 


 


 


 


 


├


─


─


 


l


i


b


/


 
 
 
 
├
─
─
 
f
o
n
t
/


 


 


 


 


 


 


 


 


├


─


─


 


N


o


t


o


S


a


n


s


J


P


-


R


e


g


u


l


a


r


.


t


t


f






 


 


 


 


 


 


 


 


├


─


─


 


N


o


t


o


S


a


n


s


J


P


-


R


e


g


u


l


a


r


.


c


w


1


2


7


.


p


k


l






 


 


 


 


 


 


 


 


├


─


─


 


-


F


6


j


f


j


t


q


L


z


I


2


J


P


C


g


Q


B


n


w


7


H


F


y


z


S


D


-


A


s


r


e


g


P


8


V


F


B


E


j


7


5


v


Y


0


r


w


-


o


M


E


.


t


t


f






 


 


 


 


 


 


 


 


├


─


─


 


N


o


t


o


S


a


n


s


J


P


-


R


e


g


u


l


a


r


.


p


k


l


 
 
 
 
├
─
─
 
c
k
e
d
i
t
o
r
/


 


 


 


 


 


 


 


 


├


─


─


 


f


i


l


e


-


i


c


o


n


s


/






 


 


 


 


 


 


 


 


├


─


─


 


c


k


e


d


i


t


o


r


/






 


 


 


 


 


 


 


 


├


─


─


 


c


k


e


d


i


t


o


r


-


i


n


i


t


.


j


s






 


 


 


 


 


 


 


 


├


─


─


 


g


a


l


l


e


r


i


f


f


i


c


/






 


 


 


 


 


 


 


 


├


─


─


 


c


k


e


d


i


t


o


r


_


u


p


l


o


a


d


e


r


/


 
 
 
 
├
─
─
 
a
d
m
i
n
/


 


 


 


 


 


 


 


 


├


─


─


 


f


o


n


t


s


/






 


 


 


 


 


 


 


 


├


─


─


 


i


m


g


/






 


 


 


 


 


 


 


 


├


─


─


 


c


s


s


/






 


 


 


 


 


 


 


 


├


─


─


 


d


a


t


a


_


f


i


l


e


s


/






 


 


 


 


 


 


 


 


├


─


─


 


j


s


/


 
 
 
 
├
─
─
 
l
i
b
r
a
r
y
/


 


 


 


 


 


 


 


 


├


─


─


 


d


e


l


e


t


e


_


b


o


o


k


s


.


x


l


s


x






 


 


 


 


 


 


 


 


├


─


─


 


i


m


p


o


r


t


_


b


o


o


k


s


.


x


l


s


x


 
 
 
 
├
─
─
 
p
r
i
c
e
/


 


 


 


 


 


 


 


 


├


─


─


 


i


m


a


g


e


s


/


 
 
 
 
├
─
─
 
c
h
a
t
/


 


 


 


 


 


 


 


 


├


─


─


 


c


s


s


/






 


 


 


 


 


 


 


 


├


─


─


 


j


s


/






 


 


 


 


 


 


 


 


├


─


─


 


i


m


a


g


e


s


/


 
 
 
 
├
─
─
 
t
a
g
i
f
y
/


 


 


 


 


 


 


 


 


├


─


─


 


c


s


s


/






 


 


 


 


 


 


 


 


├


─


─


 


j


s


/


 
 
 
 
├
─
─
 
c
s
s
/


 


 


 


 


 


 


 


 


├


─


─


 


b


e


t


a


.


c


s


s






 


 


 


 


 


 


 


 


├


─


─


 


c


o


m


m


o


n


.


c


s


s






 


 


 


 


 


 


 


 


├


─


─


 


p


r


i


n


t


2


.


c


s


s






 


 


 


 


 


 


 


 


├


─


─


 


r


e


d


m


o


n


d


/






 


 


 


 


 


 


 


 


├


─


─


 


c


o


m


m


o


n


_


o


l


d


[


.


c


s


s






 


 


 


 


 


 


 


 


├


─


─


 


c


a


n


c


e


l


_


d


o


c


.


c


s


s






 


 


 


 


 


 


 


 


├


─


─


 


p


r


i


n


t


.


c


s


s


 
 
 
 
├
─
─
 
m
o
d
e
l
s
/


 


 


 


 


 


 


 


 


├


─


─


 


f


a


c


e


_


d


e


t


e


c


t


i


o


n


_


y


u


n


e


t


_


2


0


2


3


m


a


r


.


o


n


n


x


 
 
 
 
├
─
─
 
j
s
/


 


 


 


 


 


 


 


 


├


─


─


 


t


o


o


l


s


.


j


s






 


 


 


 


 


 


 


 


├


─


─


 


j


q


u


e


r


y


-


u


i


-


1


.


1


0


.


4


.


c


u


s


t


o


m


.


m


i


n


.


j


s






 


 


 


 


 


 


 


 


├


─


─


 


i


n


i


t


.


j


s






 


 


 


 


 


 


 


 


├


─


─


 


c


o


m


m


o


n


.


j


s






 


 


 


 


 


 


 


 


├


─


─


 


d


a


t


e


p


i


c


k


e


r


.


j


s






 


 


 


 


 


 


 


 


├


─


─


 


f


i


r


e


b


a


s


e


-


m


e


s


s


a


g


i


n


g


-


s


w


.


j


s


 
 
 
 
├
─
─
 
n
e
s
t
e
d
_
a
d
m
i
n
/


 


 


 


 


 


 


 


 


├


─


─


 


d


i


s


t


/






 


 


 


 


 


 


 


 


├


─


─


 


s


r


c


/


 
 
 
 
├
─
─
 
s
k
i
l
l
_
c
h
e
c
k
/


 


 


 


 


 


 


 


 


├


─


─


 


c


s


s


/


 
 
 
 
├
─
─
 
c
o
r
p
/


 


 


 


 


 


 


 


 


├


─


─


 


c


o


m


m


o


n


/


 
 
 
 
├
─
─
 
i
m
a
g
e
s
/


 


 


 


 


 


 


 


 


├


─


─


 


c


h


a


n


g


e


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


s


o


r


t


_


a


s


c


d


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


i


b


j


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


f


a


c


e


/






 


 


 


 


 


 


 


 


├


─


─


 


e


q


_


n


o


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


l


i


s


t


2


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


I


B


J


_


l


o


g


o


_


h


a


n


k


o


u


.


P


N


G






 


 


 


 


 


 


 


 


├


─


─


 


l


i


n


k


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


i


n


t


r


o


_


f


u


l


l


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


h


e


a


d


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


d


o


w


n


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


i


a


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


e


q


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


o


d


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


l


o


g


o


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


e


d


i


t


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


i


n


t


e


r


n


e


t


_


a


c


a


d


e


m


y


_


a


d


d


r


e


s


s


.


P


N


G






 


 


 


 


 


 


 


 


├


─


─


 


u


p


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


d


o


w


n


_


n


o


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


4


0


4


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


s


t


a


r


s


/






 


 


 


 


 


 


 


 


├


─


─


 


s


o


r


t


_


a


s


c


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


b


e


t


a


/






 


 


 


 


 


 


 


 


├


─


─


 


h


e


a


r


t


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


s


p


a


c


e


r


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


T


h


u


m


b


s


.


d


b






 


 


 


 


 


 


 


 


├


─


─


 


I


A


_


l


o


g


o


_


h


a


n


k


o


u


.


P


N


G






 


 


 


 


 


 


 


 


├


─


─


 


l


o


g


o


_


b


k


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


i


a


_


l


o


g


o


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


l


i


s


t


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


d


l


o


a


d


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


h


a


n


k


o


.


P


N


G






 


 


 


 


 


 


 


 


├


─


─


 


t


o


o


l


t


i


p


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


i


n


t


e


r


n


e


t


_


a


c


a


d


e


m


y


_


c


o


n


t


a


c


t


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


s


p


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


i


n


t


r


o


_


l


e


f


t


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


a


p


p


l


y


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


s


o


r


t


_


b


o


t


h


.


p


n


g






 


 


 


 


 


 


 


 


├


─


─


 


u


p


_


n


o


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


s


o


r


t


_


d


e


s


c


.


g


i


f






 


 


 


 


 


 


 


 


├


─


─


 


s


o


r


t


_


d


e


s


c


d


.


p


n


g


 
 
 
 
├
─
─
 
r
e
s
t
_
f
r
a
m
e
w
o
r
k
/


 


 


 


 


 


 


 


 


├


─


─


 


f


o


n


t


s


/






 


 


 


 


 


 


 


 


├


─


─


 


i


m


g


/






 


 


 


 


 


 


 


 


├


─


─


 


c


s


s


/






 


 


 


 


 


 


 


 


├


─


─


 


j


s


/






 


 


 


 


 


 


 


 


├


─


─


 


d


o


c


s


/


 
 
 
 
├
─
─
 
f
o
n
t
a
w
e
s
o
m
e
-
5
.
1
5
.
2
/


 


 


 


 


 


 


 


 


├


─


─


 


a


t


t


r


i


b


u


t


i


o


n


.


j


s






 


 


 


 


 


 


 


 


├


─


─


 


l


e


s


s


/






 


 


 


 


 


 


 


 


├


─


─


 


s


v


g


s


/






 


 


 


 


 


 


 


 


├


─


─


 


c


s


s


/






 


 


 


 


 


 


 


 


├


─


─


 


s


p


r


i


t


e


s


/






 


 


 


 


 


 


 


 


├


─


─


 


m


e


t


a


d


a


t


a


/






 


 


 


 


 


 


 


 


├


─


─


 


L


I


C


E


N


S


E


.


t


x


t






 


 


 


 


 


 


 


 


├


─


─


 


j


s


/






 


 


 


 


 


 


 


 


├


─


─


 


s


c


s


s


/






 


 


 


 


 


 


 


 


├


─


─


 


w


e


b


f


o


n


t


s


/


 
 
 
 
├
─
─
 
b
o
h
r
/


 


 


 


 


 


 


 


 


├


─


─


 


c


o


m


m


o


n


_


b


o


h


r


/
├── __init__.py
├── migrate_work_to_document_upload.py
├── bohr_common/
 
 
 
 
├
─
─
 
m
i
g
r
a
t
i
o
n
s
/


 


 


 


 


 


 


 


 


├


─


─


 


_


_


i


n


i


t


_


_


.


p


y


 
 
 
 
├
─
─
 
v
i
e
w
s
/


 


 


 


 


 


 


 


 


├


─


─


 


I


T


_


t


e


s


t


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


_


_


i


n


i


t


_


_


.


p


y


 
 
 
 
├
─
─
 
f
u
n
c
t
i
o
n
s
.
p
y


 
 
 
 
├
─
─
 
a
p
p
s
.
p
y


 
 
 
 
├
─
─
 
s
e
r
i
a
l
i
z
e
r
s
.
p
y


 
 
 
 
├
─
─
 
u
r
l
s
.
p
y


 
 
 
 
├
─
─
 
_
_
i
n
i
t
_
_
.
p
y


 
 
 
 
├
─
─
 
m
o
d
e
l
s
.
p
y
├── pyproject.toml
├── chatbot_credentials.json
├── bohr/
 
 
 
 
├
─
─
 
a
p
p
s
/


 


 


 


 


 


 


 


 


├


─


─


 


b


o


h


r


_


c


o


r


e


/






 


 


 


 


 


 


 


 


├


─


─


 


s


t


u


d


e


n


t


/






 


 


 


 


 


 


 


 


├


─


─


 


c


o


n


t


e


s


t


/






 


 


 


 


 


 


 


 


├


─


─


 


_


_


i


n


i


t


_


_


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


q


u


i


z


/


 
 
 
 
├
─
─
 
e
m
a
i
l
_
d
a
t
a
.
p
y


 
 
 
 
├
─
─
 
t
e
m
p
l
a
t
e
s
/


 


 


 


 


 


 


 


 


├


─


─


 


b


o


h


r


_


c


o


r


e


/






 


 


 


 


 


 


 


 


├


─


─


 


m


o


b


i


l


e


_


a


p


p


/






 


 


 


 


 


 


 


 


├


─


─


 


s


t


u


d


e


n


t


/






 


 


 


 


 


 


 


 


├


─


─


 


c


o


n


t


e


s


t


/






 


 


 


 


 


 


 


 


├


─


─


 


o


d


/






 


 


 


 


 


 


 


 


├


─


─


 


m


e


m


b


e


r


/






 


 


 


 


 


 


 


 


├


─


─


 


e


r


r


o


r


.


h


t


m


l






 


 


 


 


 


 


 


 


├


─


─


 


b


o


h


r


_


c


o


m


m


o


n


/






 


 


 


 


 


 


 


 


├


─


─


 


q


u


i


z


/


 
 
 
 
├
─
─
 
_
_
i
n
i
t
_
_
.
p
y


 
 
 
 
├
─
─
 
u
t
i
l
s
.
p
y


 
 
 
 
├
─
─
 
e
m
a
i
l
/


 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


o


t


p


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


d


o


c


_


a


p


p


l


y


_


s


t


a


f


f


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


d


o


c


_


a


p


p


l


y


_


e


n


r


o


l


l


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


d


o


c


_


a


p


p


l


y


_


e


d


u


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


t


r


a


n


s


f


e


r


.


p


y






 


 


 


 


 


 


 


 


├


─


─


 


e


m


a


i


l


_


v


e


r


i


f


y


.


p


y
```
