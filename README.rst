PyTraceTable
===========================

PyTraceTable is a tool for scripting and script debugging. It aims to make a line-by-line debugging easier.

Take a look:

.. code:: python

    from pytracetable import tracetable

    @tracetable()
    def some_weird_calculation(a, b):
            c = 10 + a
            b *= 2
            c += b
            del b
            return a + c
    

Then, calling :code:`some_weird_calculation(5, 10)` will give the output:

.. code::

    --------------------------------------------------
    At some_weird_calculation, line 3
        [ADDED]    a (int): 5
        [ADDED]    b (int): 10
     
    --------------------------------------------------
    At some_weird_calculation, line 4
        [ADDED]    c (int): 15
     
    --------------------------------------------------
    At some_weird_calculation, line 5
        [CHANGED]  b: 10 (int) --> 20 (int)
     
    --------------------------------------------------
    At some_weird_calculation, line 6
        [CHANGED]  c: 15 (int) --> 35 (int)
     
    --------------------------------------------------
    At some_weird_calculation, line 7
        [REMOVED]  b
        [RETURNED] 40 (int)


Contribute
----------

Did you think in some interesting feature, or have you found a bug? Please let me know!

Of course you can also download the project and send me some `pull requests <https://github.com/filwaitman/pytracetable/pulls>`_.


You can send your suggestions by `opening issues <https://github.com/filwaitman/pytracetable/issues>`_.

You can contact me directly as well. Take a look at my contact information at `http://filwaitman.github.io/ <http://filwaitman.github.io/>`_ (email is preferred rather than mobile phone).
