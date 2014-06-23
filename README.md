sms-tools
========= 

<p>Spectral modeling analysis and synthesis tools written in python
and C for sound and music applications, plus complementary teaching
material.</p>

<p>In order to use all the software you have to install version 2.7
of python and the following modules: ipython, matplotlib, Numpy,
Scipy. 
</p>
<p>
In Ubuntu (which we recommend) to install all the modules is as simple as typing in 
the terminal:</p>
<p>
<code class="western">
sudo apt-get install python-dev python-setuptools build-essentia ipython python-matplotlib python-numpy python-scipy
</code>
</p>
<p>Some of the core functions are written in C (software/models/utilFunctions_C( and have to be compiled. For that,
you first have to install Cython, by typing on a Terminal: </p>
<p>
<code class="western">
easy_install cython
</code>
</p>
Once Cython is installed, in the Terminal go to the directory
software/models/utilFunctions_C and type:</p>
<p>
<code class="western">python
compileModule.py build_ext --inplace </code>
</p>

<p>The code for the basic analysis/synthesis models is in the
directory software/models. There are examples of analysis/transformation/synthesis in the
examples directory. All the sounds used in the examples are in the
sounds directory.</p>

<p>To start we recommend to download the whole package, then create a folder with the name workspace 
within the main folder, then copy one of the examples into the workspace folder, go to this folder in the Terminal and type: </p>
<code class="western">python
"example.py" </code>
</p>

<p>All this code is used in several classes that I teach. The slides
and demo code used in class are in the lectures directory.</p>

