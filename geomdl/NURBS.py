"""
.. module:: NURBS
    :platform: Unix, Windows
    :synopsis: A data storage and evaluation class for NURBS curves and surfaces

.. moduleauthor:: Onur Rauf Bingol

"""

import sys
import geomdl.BSpline as BSpline
import geomdl.utilities as utils


class Curve(BSpline.Curve):
    """ A data storage and evaluation class for 3D NURBS curves.

    **Data Storage**

    :class:`.Curve` class implements Python properties using the ``@property`` decorator. The following properties are present in this class:

    * order
    * degree
    * knotvector
    * delta
    * ctrlpts
    * weights
    * curvepts

    The function :func:`.read_ctrlpts()` provides an easy way to read weighted control points from a text file.
    Additional details for the text format can be found in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.

    **Evaluation**

    The evaluation methods in the :class:`.Curve` class are:

    * :func:`.evaluate()`
    * :func:`.derivatives()`
    * :func:`.tangent()`

    Please check the function reference for the details.

    .. note::

        If you update any of the data storage elements after the curve evaluation, the surface points stored in :py:attr:`~curvepts` property will be deleted automatically.
    """
    def __init__(self):
        super(Curve, self).__init__()
        # Override dimension variable
        self._mDimension = 4  # 3D coordinates + weights

    @property
    def ctrlpts(self):
        """ Control points

        Control points of a :class:`.Curve` is stored as a list of (x*w, y*w, z*w, w) coordinates

        :getter: Gets the control points in (x, y, z) format. Use :py:attr:`~weights` to get weights vector.
        :setter: Sets the control points in (x*w, y*w, z*w, w) format
        :type: list
        """
        ret_list = []
        for pt in self._mCtrlPts:
            temp = []
            idx = 0
            while idx < self._mDimension - 1:
                temp.append(float(pt[idx] / pt[-1]))
                idx += 1
            ret_list.append(tuple(temp))
        return tuple(ret_list)

    @property
    def weights(self):
        """ Weights vector

        :getter: Extracts the weights vector from weighted control points array
        :type: list
        """
        weights = []
        for pt in self._mCtrlPts:
            weights.append(pt[-1])
        return tuple(weights)

    # Evaluates the NURBS curve
    def evaluate(self):
        """ Evaluates the NURBS curve.

        .. note:: The evaluated surface points are stored in :py:attr:`~curvepts`.

        :return: None
        """
        # Check all parameters are set before the curve evaluation
        self._check_variables()
        # Clean up the curve points, if necessary
        self._reset_curve()

        # Algorithm A4.1
        for u in utils.frange(0, 1, self._mDelta):
            span = utils.find_span(self._mDegree, tuple(self._mKnotVector), len(self._mCtrlPts), u)
            basis = utils.basis_functions(self._mDegree, tuple(self._mKnotVector), span, u)
            cptw = [0.0 for x in range(self._mDimension)]
            for i in range(0, self._mDegree + 1):
                idx = 0
                while idx < self._mDimension:
                    cptw[idx] += (basis[i] * self._mCtrlPts[span - self._mDegree + i][idx])
                    idx += 1
            # Divide by weight
            curvept = []
            idx = 0
            while idx < self._mDimension - 1:
                curvept.append(float(cptw[idx] / cptw[-1]))
                idx += 1
            self._mCurvePts.append(curvept)

    # Evaluates the rational curve derivative
    def derivatives(self, u=-1, order=0):
        """ Evaluates n-th order curve derivatives at the given u from the rational curve.

        :param u: knot value
        :type u: float
        :param order: derivative order
        :type order: integer
        :return: A list containing up to {order}-th derivative of the curve
        :rtype: list
        """
        # Call the parent function to evaluate A(u) and w(u) derivatives
        CKw = super(Curve, self).derivatives(u, order)

        # Algorithm A4.2
        CK = [[None for x in range(self._mDimension-1)] for y in range(order + 1)]
        for k in range(0, order + 1):
            v = []
            idx = 0
            while idx < self._mDimension - 1:
                v.append(CKw[idx])
                idx += 1

            for i in range(1, order + 1):
                idx = 0
                while idx < self._mDimension - 1:
                    v[idx] -= (utils.binomial_coeff(k, i) * CKw[i][-1] * CK[k-i][idx])
                    idx += 1

            idx = 0
            while idx < self._mDimension - 1:
                CK[k][idx] = v[idx] / CKw[0][-1]
                idx += 1

        # Return C(u) derivatives
        return CK


class Curve2D(Curve):
    """ A data storage and evaluation class for 2D NURBS curves.

    This class is a subclass of :class:`.Curve` with only the dimensional change.
    """
    def __init__(self):
        super(Curve2D, self).__init__()
        # Override dimension variable
        self._mDimension = 3  # 2D coordinates + weights


class Surface(BSpline.Surface):
    """ A data storage and evaluation class for NURBS surfaces.

    **Data Storage**

    :class:`.Surface` class implements Python properties using the ``@property`` decorator. The following properties are present in this class:

    * order_u
    * order_v
    * degree_u
    * degree_v
    * knotvector_u
    * knotvector_v
    * delta
    * ctrlpts
    * ctrlptsw
    * ctrlpts2D
    * weights
    * surfpts

    The functions :func:`.read_ctrlpts()` and :func:`.read_ctrlptsw()` provide an easy way to read control points from a text file.
    Additional details for the text format can be found in `FORMATS.md <https://github.com/orbingol/NURBS-Python/blob/master/FORMATS.md>`_ file.

    **Evaluation**

    The evaluation methods in the :class:`.Surface` class are:

    * :func:`.evaluate()`
    * :func:`.derivatives()`
    * :func:`.tangent()`
    * :func:`.normal()`

    .. note::

        If you update any of the data storage elements after the surface evaluation, the surface points stored in :py:attr:`~surfpts` property will be deleted automatically.
    """
    def __init__(self):
        super(Surface, self).__init__()
        # Override dimension variable
        self._mDimension = 4  # 3D coordinates + weights

    @property
    def ctrlpts(self):
        """ Control points

        Control points of a :class:`.Surface` is stored as a list of (x*w, y*w, z*w, w) coordinates

        :getter: Gets the control points in (x, y, z) format. Use :py:attr:`~weights` to get weights vector.
        :setter: Sets the control points in (x*w, y*w, z*w, w) format
        :type: list
        """
        ret_list = []
        for pt in self._mCtrlPts:
            temp = []
            idx = 0
            while idx < self._mDimension - 1:
                temp.append(float(pt[idx] / pt[-1]))
                idx += 1
            ret_list.append(tuple(temp))
        return tuple(ret_list)

    @property
    def weights(self):
        """ Weights vector

        :getter: Extracts the weights vector from weighted control points array
        :type: list
        """
        weights = []
        for pt in self._mCtrlPts:
            weights.append(pt[-1])
        return tuple(weights)

    # Evaluates the NURBS surface
    def evaluate(self):
        """ Evaluates the NURBS surface.

        .. note:: The evaluated surface points are stored in :py:attr:`~surfpts`.

        :return: None
        """
        # Check all parameters are set before the surface evaluation
        self._check_variables()
        # Clean up the surface points lists, if necessary
        self._reset_surface()

        # Algorithm A4.3
        for v in utils.frange(0, 1, self._mDelta):
            span_v = utils.find_span(self._mDegreeV, tuple(self._mKnotVectorV), self._mCtrlPts_sizeV, v)
            basis_v = utils.basis_functions(self._mDegreeV, tuple(self._mKnotVectorV), span_v, v)
            for u in utils.frange(0, 1, self._mDelta):
                span_u = utils.find_span(self._mDegreeU, tuple(self._mKnotVectorU), self._mCtrlPts_sizeU, u)
                basis_u = utils.basis_functions(self._mDegreeU, tuple(self._mKnotVectorU), span_u, u)
                idx_u = span_u - self._mDegreeU
                sptw = [0.0 for x in range(self._mDimension)]
                for l in range(0, self._mDegreeV + 1):
                    temp = [0.0 for x in range(self._mDimension)]
                    idx_v = span_v - self._mDegreeV + l
                    for k in range(0, self._mDegreeU + 1):
                        idx = 0
                        while idx < self._mDimension:
                            temp[idx] += (basis_u[k] * self._mCtrlPts2D[idx_u + k][idx_v][idx])
                            idx += 1
                    idx = 0
                    while idx < self._mDimension:
                        sptw[idx] += (basis_v[l] * temp[idx])
                        idx += 1
                # Divide by weight to obtain 3D surface points
                surfpt = []
                idx = 0
                while idx < self._mDimension - 1:
                    surfpt.append(float(sptw[idx] / sptw[-1]))
                    idx += 1
                self._mSurfPts.append(surfpt)

    # Evaluates n-th order rational surface derivatives at the given (u,v) parameter
    def derivatives(self, u=-1, v=-1, order=0):
        """ Evaluates n-th order surface derivatives at the given (u,v) parameter from the rational surface.

        * SKL[0][0] will be the surface point itself
        * SKL[0][1] will be the 1st derivative w.r.t. v
        * SKL[2][1] will be the 2nd derivative w.r.t. u and 1st derivative w.r.t. v

        :param u: parameter in the U direction
        :type u: float
        :param v: parameter in the V direction
        :type v: float
        :param order: derivative order
        :type order: integer
        :return: A list SKL, where SKL[k][l] is the derivative of the surface S(u,v) w.r.t. u k times and v l times
        :rtype: list
        """
        # Call the parent function to evaluate A(u) and w(u) derivatives
        SKLw = super(Surface, self).derivatives(u, v, order)

        # Algorithm A4.4
        du = min(self._mDegreeU, order)
        dv = min(self._mDegreeV, order)

        # Generate an empty list of derivatives
        SKL = [[[None for x in range(self._mDimension)] for y in range(dv + 1)] for z in range(du + 1)]

        for k in range(0, order + 1):
            for l in range(0, order - k + 1):
                v = []
                idx = 0
                while idx < self._mDimension - 1:
                    v.append(SKLw[idx])
                    idx += 1

                for j in range(1, l + 1):
                    idx = 0
                    while idx < self._mDimension - 1:
                        v[idx] -= (utils.binomial_coeff(l, j) * SKLw[0][j][-1] * SKL[k][l - j][idx])
                        idx += 1
                for i in range(1, k + 1):
                    idx = 0
                    while idx < self._mDimension - 1:
                        v[idx] -= (utils.binomial_coeff(k, i) * SKLw[i][0][-1] * SKL[k - i][l][idx])
                        idx += 1
                    v2 = [0.0 for x in range(self._mDimension - 1)]
                    for j in range(1, l + 1):
                        idx = 0
                        while idx < self._mDimension - 1:
                            v2[idx] += (utils.binomial_coeff(l, j) * SKLw[i][j][-1] * SKL[k - i][l - j][idx])
                            idx += 1
                    idx = 0
                    while idx < self._mDimension - 1:
                        v[idx] -= (utils.binomial_coeff(k, i) * v2[idx])
                        idx += 1

                idx = 0
                while idx < self._mDimension - 1:
                    SKL[k][l][idx] = v[idx] / SKLw[0][0][-1]
                    idx += 1

        # Return S(u,v) derivatives
        return SKL