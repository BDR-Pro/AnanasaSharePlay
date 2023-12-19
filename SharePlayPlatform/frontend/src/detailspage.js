import 'bootstrap/dist/css/bootstrap.min.css';
import Detail from './components/detail';
import React from 'react';


// Access the slug value from Django
const slug = window.slugFromDjango;

ReactDOM.render(<Detail slug={slug} />, document.getElementById('detail'));