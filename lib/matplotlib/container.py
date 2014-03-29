from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

import matplotlib.cbook as cbook


class Container(tuple):
    """
    Base class for containers.
    """

    def __repr__(self):
        return "<Container object of %d artists>" % (len(self))

    def __new__(cls, *kl, **kwargs):
        return tuple.__new__(cls, kl[0])

    def __init__(self, kl, label=None):

        self.eventson = False  # fire events only if eventson
        self._oid = 0  # an observer id
        self._propobservers = {}  # a dict from oids to funcs

        self._remove_method = None

        self.set_label(label)

    def set_remove_method(self, f):
        self._remove_method = f

    def remove(self):
        for c in self:
            c.remove()

        if self._remove_method:
            self._remove_method(self)

    def __getstate__(self):
        d = self.__dict__.copy()
        # remove the unpicklable remove method, this will get re-added on load
        # (by the axes) if the artist lives on an axes.
        d['_remove_method'] = None
        return d

    def get_label(self):
        """
        Get the label used for this artist in the legend.
        """
        return self._label

    def set_label(self, s):
        """
        Set the label to *s* for auto legend.

        ACCEPTS: string or anything printable with '%s' conversion.
        """
        if s is not None:
            self._label = '%s' % (s, )
        else:
            self._label = None
        self.pchanged()

    def add_callback(self, func):
        """
        Adds a callback function that will be called whenever one of
        the :class:`Artist`'s properties changes.

        Returns an *id* that is useful for removing the callback with
        :meth:`remove_callback` later.
        """
        oid = self._oid
        self._propobservers[oid] = func
        self._oid += 1
        return oid

    def remove_callback(self, oid):
        """
        Remove a callback based on its *id*.

        .. seealso::

            :meth:`add_callback`
               For adding callbacks

        """
        try:
            del self._propobservers[oid]
        except KeyError:
            pass

    def pchanged(self):
        """
        Fire an event when property changed, calling all of the
        registered callbacks.
        """
        for oid, func in list(six.iteritems(self._propobservers)):
            func(self)

    def get_children(self):
        return list(cbook.flatten(self))


class BarContainer(Container):

    def __init__(self, patches, errorbar=None, **kwargs):
        self.patches = patches
        self.errorbar = errorbar
        Container.__init__(self, patches, **kwargs)

class HistContainer(Container):

    def __init__(self,
                 x=None,
                 nbins=None,
                 range=None,
                 normed=None,
                 weights=None,
                 cumulative=None,
                 bottom=None,
                 histtype=None,
                 align=None,
                 orientation=None,
                 rwidth=None,
                 log=None,
                 color=None,
                 label=None,
                 stacked=None,
                 patches=None,
                 errorbar=None,
                 **kwargs):
        self.x=x
        self.nbins=nbins
        self.range=range
        self.normed=normed
        self.weights=weights
        self.cumulative=cumulative
        self.bottom=bottom
        self.histtype=histtype
        self.align=align
        self.orientation=orientation
        self.rwidth=rwidth
        self.log=log
        self.color=color
        self.label=label
        self.stacked=stacked
        self.errorbar=errorbar

        Container.__init__(self, patches, **kwargs)

class ScatterContainer(Container):

    def __init__(self,
                 x=None,
                 y=None,
                 s=None,
                 c=None,
                 marker=None,
                 cmap=None,
                 norm=None,
                 vmin=None,
                 vmax=None,
                 alpha=None,
                 linewidths=None,
                 verts=None,
                 **kwargs):
        self.x=x
        self.y=y
        self.s=s
        self.c=c
        self.marker=marker
        self.cmap=cmap
        self.norm=norm
        self.vmin=vmin
        self.vmax=vmax
        self.alpha=alpha
        self.linewidths=linewidths
        self.verts=verts
        Container.__init__(self, **kwargs)

class ErrorbarContainer(Container):

    def __init__(self,
                 lines,
                 has_xerr=False,
                 has_yerr=False,
                 **kwargs):
        self.lines = lines
        self.has_xerr = has_xerr
        self.has_yerr = has_yerr
        Container.__init__(self, lines, **kwargs)


class StemContainer(Container):

    def __init__(self, markerline_stemlines_baseline, **kwargs):
        markerline, stemlines, baseline = markerline_stemlines_baseline
        self.markerline = markerline
        self.stemlines = stemlines
        self.baseline = baseline
        Container.__init__(self, markerline_stemlines_baseline, **kwargs)
