## Installation

create environment:

<pre>
    python -m venv venv
</pre>


activate environment windows:

<pre>
    venv\Scripts\activate
</pre>

Install requirements:

<pre>
    pip install -r requirements.txt
</pre>

Backend server 

<pre>
    python -m uvicorn backend.main:app --reload 
</pre>


Frontend server 

<pre>
    python -m http.server 5500
</pre>