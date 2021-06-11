from manimlib import *
from math import *

class OpenScene(Scene):
    def construct(self):
        f = Tex('f')
        fPrime = Tex('df \over dx')

        """
        SCRIPT:
        tim hieu ve dao ham va thong tin...
        """
        self.play(ShowCreation(f))
        self.play(Transform(f, fPrime))
        self.play(FadeOut(f), FadeOut(fPrime))

        x_range = (0, 10)
        y_range = (0, 10)
        x_min = [7.47]
        x_max = [2.663]
        x_criticals = x_max + x_min

        def func(x):
            def aux(x):
                return x**3 - 4*x**2 + x + 3
            return aux(0.5*x - 1.2) + 5

        axes = Axes (
            x_range, y_range,
            height=6,
            width=5
        )
        axes.add_coordinate_labels()

        graph = axes.get_graph(func, color=BLUE)
        label = axes.get_graph_label(graph, "f(x)")

        self.play(Write(axes), Write(label))

        trackers = [ValueTracker(val) for val in x_criticals]
        trackerDots = [Dot(color=RED), Dot(color=RED)]
        f_always(
            trackerDots[0].move_to,
            lambda : axes.i2gp(trackers[0].get_value(), graph)
        )
        f_always(
            trackerDots[1].move_to,
            lambda : axes.i2gp(trackers[1].get_value(), graph)
        )

        maxPointLabel = Text("Cực đại", font_size=25)
        maxPointLabel.next_to(trackerDots[0], UP)
        minPointLabel = Text("Cực tiểu", font_size=25)
        minPointLabel.next_to(trackerDots[1], RIGHT)
        """
        SCRIPT:
         do la cuc tri
        """
        self.play(
            FadeIn(graph),
            FadeIn(label),
            *[FadeIn(trackerDot, scale=0.5) for trackerDot in trackerDots],
        )
        """
        SCRIPT:
        cuc tri la ten goi chung cua ....
        """
        self.play(
            *[Write(pointLabel) for pointLabel in [maxPointLabel, minPointLabel]]
        )

        criticalPointLabel = Text("Cực Trị")
        criticalPointLabel.to_corner(UR)
        arr1 = Arrow(criticalPointLabel, maxPointLabel)
        arr2 = Arrow(criticalPointLabel, minPointLabel)
        self.play(ShowCreation(criticalPointLabel), Write(arr1), Write(arr2))


def func(x):
    return 0.3*x**3 - 3.23*x**2 + 8.6*x + 1


class PresentationOfProblem(Scene):
    def construct(self):
        """
        SCRIPT: gia su chung ta co ham sau day
        :return:
        """
        x_range = (0, 7)
        y_range = (0, 10)
        x_min = [5.412]
        x_max = [1.766]
        x_criticals = x_max + x_min

        funcForm = Tex("f(x) = 0.3x^3 - 3.23x^2 + 8.6x + 1")
        axes = Axes(
            x_range, y_range,
            height=6,
            width=5
        )
        axes.add_coordinate_labels()
        VGroup(funcForm, axes).arrange(UP)

        graph = axes.get_graph(func, color=BLUE)

        trackers = [ValueTracker(val) for val in x_criticals]
        trackerDots = [Dot(color=RED), Dot(color=RED)]
        f_always(
            trackerDots[0].move_to,
            lambda: axes.i2gp(trackers[0].get_value(), graph)
        )
        f_always(
            trackerDots[1].move_to,
            lambda: axes.i2gp(trackers[1].get_value(), graph)
        )
        vertLines = [
            always_redraw(lambda: axes.get_v_line(trackerDots[0].get_bottom())),
            always_redraw(lambda: axes.get_v_line(trackerDots[1].get_bottom()))
        ]
        questionMarks = [
            Text("?"), Text("?")
        ]
        for qm, dot in zip(questionMarks, trackerDots):
            qm.next_to(dot)

        self.play(
            Write(axes),
            Write(funcForm),
            ShowCreation(graph)
        )

        self.play(
            *[FadeIn(vertLine) for vertLine in vertLines],
            *[FadeIn(trackerDot) for trackerDot in trackerDots]
        )
        """
        SCRIPT: chung ta muon biet vao thoi diem nao so luong gao la cao nhat va
        """
        self.play(*[FadeIn(qm) for qm in questionMarks])

class ReviewFromLastLecture(Scene):
    def construct(self):
        def curve(x):
            return -(0.75*x-4)**2 + 8

        x_range = (0, 11)
        y_range = (0, 10)

        axes = Axes(x_range, y_range, height=6, width=5)
        axes.add_coordinate_labels()

        graph = axes.get_graph(curve, color=BLUE)

        label = axes.get_graph_label(graph, "p(t)")

        self.play(Write(axes), Write(label))
        self.play(ShowCreation(graph, lag_ratio=0.05))
        self.wait()

        # tangent line
        tracker_dot = Dot(color=RED)
        tracker_dot.move_to(axes.i2gp(0, graph))

        tracker = ValueTracker(2)
        f_always(
            tracker_dot.move_to,
            lambda: axes.i2gp(tracker.get_value(), graph)
        )
        vert_line = always_redraw(lambda: axes.get_v_line(tracker_dot.get_bottom()))

        tan_line = always_redraw(
            lambda:
            TangentLine(
                graph,
                tracker.get_value() / (x_range[1] - x_range[0]),
                length=2, stroke_capacity=0.75
            )
        )

        slope_text, slope_val = slope_label = VGroup(
            Text("Độ dốc = ", font_size=25),
            DecimalNumber(
                0,
                show_ellipsis=False,
                num_decimal_places=1,
                include_sign=True,
                font_size=25
            )
        )
        slope_label.arrange(RIGHT)
        always(slope_label.next_to, axes, UP)
        f_always(slope_val.set_value, tan_line.get_slope)

        self.play(
            FadeIn(tan_line, scale=0.5),
            FadeIn(vert_line, scale=0.5),
            FadeIn(tracker_dot, scale=0.5),
            Write(slope_label)
        )

        # slope > 0
        """
        SCRIPT:
        khi dao ham la so duong, ham tang ...
        """
        sign_gt_zero = Text(" > 0", font_size=25)
        sign_gt_zero.next_to(slope_label, RIGHT)
        self.play(FadeIn(sign_gt_zero))
        self.play(
            tracker.animate.set_value(5),
            run_time=4,
            rate_func=there_and_back_with_pause
        )
        """
        SCRIPT: khi dao ham la so am, ham dang giam.
        """
        sign_lt_zero = Text(" < 0", font_size=25)
        sign_lt_zero.next_to(slope_label, RIGHT)
        self.play(
            tracker.animate.set_value(6),
            ReplacementTransform(sign_gt_zero, sign_lt_zero),
            run_time=3,
            rate_func=smooth
        )
        self.play(
            tracker.animate.set_value(9),
            run_time=6,
            rate_func=there_and_back
        )

        # slope = 0
        """
        SCRIPT: khi dao ham = 0, ham ko thay doi
        """
        sign_is_zero = Text(" = 0", font_size=25)
        sign_is_zero.next_to(slope_label, RIGHT)
        self.play(
            tracker.animate.set_value(5.3333),
            ReplacementTransform(sign_lt_zero, sign_is_zero),
            run_time=2
        )

        self.play(
            FadeOut(tan_line)
        )

class Observation(Scene):
    def construct(self):
        x_range = (0, 7)
        y_range = (0, 10)
        x_min = [5.412]
        x_max = [1.766]
        x_criticals = x_max + x_min

        funcForm = Tex("f(x) = 0.3x^3 - 3.23x^2 + 8.6x + 1")
        axes = Axes(
            x_range, y_range,
            height=6,
            width=5
        )
        axes.add_coordinate_labels()
        VGroup(funcForm, axes).arrange(UP)

        graph = axes.get_graph(func, color=BLUE)

        trackers = [ValueTracker(val) for val in x_criticals]
        trackerDots = [Dot(color=RED), Dot(color=RED)]
        f_always(
            trackerDots[0].move_to,
            lambda: axes.i2gp(trackers[0].get_value(), graph)
        )
        f_always(
            trackerDots[1].move_to,
            lambda: axes.i2gp(trackers[1].get_value(), graph)
        )
        vertLines = [
            always_redraw(lambda: axes.get_v_line(trackerDots[0].get_bottom())),
            always_redraw(lambda: axes.get_v_line(trackerDots[1].get_bottom()))
        ]

        maxPointLabel = Text(f'Cực đại, x = {x_max[0]}', font_size=25)
        maxPointLabel.next_to(trackerDots[0], RIGHT)
        minPointLabel = Text(f'Cực tiểu, x = {x_min[0]}', font_size=25)
        minPointLabel.next_to(trackerDots[1], RIGHT)

        self.play(
            Write(axes),
            Write(funcForm),
            ShowCreation(graph)
        )

        self.play(
            *[FadeIn(vertLine) for vertLine in vertLines],
            *[FadeIn(trackerDot) for trackerDot in trackerDots]
        )
        """
        SCRIPT: nhu cac ban se thay, ham nay co 1 diem cuc dai tai, va mot diem cuc tieu tai
        """
        self.play(
            *[Write(pointLabel) for pointLabel in [maxPointLabel, minPointLabel]]
        )



"""
SCRIPT: khi ve ra dao ham,
"""
class DerivativeSideBySide(Scene):
    def construct(self):
        x_range = (0, 7)
        y_range = (0, 10)
        x_min = [5.412]
        x_max = [1.766]
        x_criticals = x_max + x_min
        tex_font_size= 25
        funcForm = Tex("f(x) = 0.3x^3 - 3.23x^2 + 8.6x + 1", font_size=tex_font_size)
        axes = Axes(
            x_range, y_range,
            height=6,
            width=5
        )

        ## DERIVATIVE GRAPH
        derivXRange = (0, 7)
        derivYRange = (-5, 5)

        def derivFunc(x):
            return 0.9 * x ** 2 - 6.46 * x + 8.6

        derivForm = Tex("f'(x) = 0.9x^2 - 6.46x + 8.6", font_size=tex_font_size)
        derivAxes = Axes(
            derivXRange, derivYRange,
            height=6,
            width=5
        )

        # VGroup(funcForm, axes).arrange(UP)
        # VGroup(derivForm, derivAxes).arrange(UP)
        VGroup(axes, derivAxes).arrange(RIGHT, buff=1)
        VGroup(funcForm, derivForm).arrange(RIGHT, buff=1)
        funcForm.next_to(axes, DOWN, buff=0.5)
        derivForm.next_to(derivAxes, DOWN, buff=0.5)

        axes.add_coordinate_labels()
        graph = axes.get_graph(func, color=BLUE)

        derivAxes.add_coordinate_labels()
        derivGraph = derivAxes.get_graph(derivFunc, color=RED)


        self.play(
            Write(axes),
            Write(funcForm),
            Write(derivForm),
            ShowCreation(graph)
        )
        """
        SCRIPT: khi chung ta ve ra dao ham cua ham nay...
        """
        self.play(
            ShowCreation(derivAxes),
            ShowCreation(derivGraph)
        )

        ## corresponding
        ## increasing -> positive
        valueTrackers = [ValueTracker(0) for _ in range(2)]
        trackerDots = [Dot(color=RED), Dot(color=BLUE)]
        f_always(
            trackerDots[0].move_to,
            lambda : axes.i2gp(valueTrackers[0].get_value(), graph)
        )
        f_always(
            trackerDots[1].move_to,
            lambda : derivAxes.i2gp(valueTrackers[1].get_value(), derivGraph)
        )
        derivHLine = always_redraw(lambda: derivAxes.get_h_line(trackerDots[1].get_left()))

        self.play(
            ShowCreation(derivHLine),
            *[FadeIn(trackerDot, scale=0.5) for trackerDot in trackerDots]
        )
        """
        SCRIPT: khi ham dang tang, thi dao ham co gia tri duong
        """
        self.play(
            *[valueTracker.animate.set_value(1.7) for valueTracker in valueTrackers],
            run_time=3
        )
        """
        SCRIPT: khi ham dang giam, thi dao ham co gia tri am
        """
        self.play(
            *[valueTracker.animate.set_value(1.9) for valueTracker in valueTrackers],
        )
        self.play(
            *[valueTracker.animate.set_value(5) for valueTracker in valueTrackers],
            run_time=3
        )

        """
        SCRIPT: thu vi thay, ta dien x = 1.766 khi ham cuc dai, gia tri dao ham = 0
        """
        self.play(
            *[valueTracker.animate.set_value(1.766) for valueTracker in valueTrackers],
            run_time=3
        )

        """
        SCRIPT: tuong tu, khi ham cuc tieu, gia tri dao ham = 0 
        """
        self.play(
            *[valueTracker.animate.set_value(x_min[0]) for valueTracker in valueTrackers],
            run_time=3
        )

        """
        SCRIPT: hay nhin o diem x = 1.766
        """
        self.play(
            *[valueTracker.animate.set_value(1.766) for valueTracker in valueTrackers],
        )
        """
        SCRIPT: tu duong, qua am
        """
        self.play(
            *[valueTracker.animate.set_value(1.6) for valueTracker in valueTrackers],
        )
        self.play(
            *[valueTracker.animate.set_value(1.9) for valueTracker in valueTrackers],
            run_time=1
        )
        """
        SCRIPT: tuong tu, ham cuc tieu khi
        """
        self.play(
            *[valueTracker.animate.set_value(x_min[0]) for valueTracker in valueTrackers],
            run_time=3
        )
        """
        SCDIPT: khi dao ham doi dau tu AM qua Duong
        """
        self.play(
            *[valueTracker.animate.set_value(5) for valueTracker in valueTrackers],
        )
        self.play(
            *[valueTracker.animate.set_value(5.6) for valueTracker in valueTrackers],
            run_time=1
        )

        """
        SCRIPT: dieu nay de giai thich boi vi khi ham doi dau tu 
        """
        self.play(
            *[valueTracker.animate.set_value(1.766) for valueTracker in valueTrackers],
            run_time=2
        )
        """
        SCRIPT: duong qua am
        """
        self.play(
            *[valueTracker.animate.set_value(1.6) for valueTracker in valueTrackers],
        )
        self.play(
            *[valueTracker.animate.set_value(1.9) for valueTracker in valueTrackers],
            run_time=1
        )
        """
        SCRIPT: phai co 1 noi ham dat gia tri lon nhat
        """
        self.play(
            *[valueTracker.animate.set_value(x_max[0]) for valueTracker in valueTrackers],
            run_time=1
        )

        """
        SCRIPT: tuong tu, khi ham doi dau
        """
        self.play(
            *[valueTracker.animate.set_value(x_min[0]) for valueTracker in valueTrackers],
            run_time=2
        )
        """
        SCRIPT: am qua duong
        """
        self.play(
            *[valueTracker.animate.set_value(5) for valueTracker in valueTrackers],
        )
        self.play(
            *[valueTracker.animate.set_value(5.6) for valueTracker in valueTrackers],
            run_time=1
        )
        """
        SCRIPT: phai co 1 noi ham dat gia tri nho nhat
        """
        self.play(
            *[valueTracker.animate.set_value(x_min[0]) for valueTracker in valueTrackers],
            run_time=1
        )


class BraceBetweenPoints(Brace):
    """Similar to Brace, but instead of taking a mobject it uses 2
    points to place the brace.
    A fitting direction for the brace is
    computed, but it still can be manually overridden.
    If the points go from left to right, the brace is drawn from below.
    Swapping the points places the brace on the opposite side.
    Parameters
    ----------
    point_1 : Union[:class:`list`, :class:`numpy.array`]
        The first point.
    point_2 : Union[:class:`list`, :class:`numpy.array`]
        The second point.
    direction : Optional[Union[:class:`list`, :class:`numpy.array`]]
        The direction from which the brace faces towards the points.
    Examples
    --------
        .. manim:: BraceBPExample
            class BraceBPExample(Scene):
                def construct(self):
                    p1 = [0,0,0]
                    p2 = [1,2,0]
                    brace = BraceBetweenPoints(p1,p2)
                    self.play(ShowCreation(NumberPlane()))
                    self.play(ShowCreation(brace))
                    self.wait(2)
    """

    def __init__(self, point_1, point_2, direction=ORIGIN, **kwargs):
        if all(direction == ORIGIN):
            line_vector = np.array(point_2) - np.array(point_1)
            direction = np.array([line_vector[1], -line_vector[0], 0])
        Brace.__init__(self, Line(point_1, point_2), direction=direction, **kwargs)

class Para4(Scene):
    def construct(self):
        """
        SCRIPT de tim duoc cuc tri cua ham nay
        :return:
        """
        funcForm = Tex("f(x) = 0.3x^3 - 3.23x^2 + 8.6x + 1")
        derivForm = Tex("f'(x) = {{0.9x^2}} - {{6.46x}} + {{8.6}}")
        VGroup(funcForm, derivForm).arrange(DOWN)
        self.play(Write(funcForm))
        """
        SCRIPT: ta hay bat dau voi dao ham cua no
        """
        self.play(Write(derivForm))

        derivEqualZero = Tex("{{0.9x^2}} - {{6.46x}} + {{8.6}} = 0")
        self.play(FadeOut(funcForm))
        """
        SCRIPT: ep phunog trinh nay = 0
        """
        self.play(
            TransformMatchingTex(derivForm, derivEqualZero)
        )

        """
        SCRIPT: ta tim duoc 2 diem,
        theo quan sat tren, day la 2 diem cuc tri
        """
        rootA = Tex("x = 1.766")
        rootB = Tex("x = 5.412")
        roots = VGroup(rootA, rootB).arrange(RIGHT, buff=1)
        roots.next_to(derivEqualZero, DOWN)

        self.play(
            Write(rootA), Write(rootB)
        )

        """
        SCRIPT: ta dung bang bien thien nhu sau
        """
        x_min = [5.412]
        x_max = [1.766]
        x_criticals = x_max + x_min
        nl = NumberLine(
            [0, 7],
            include_tip=True,
            include_numbers=True,
            numbers_to_exclude=[]
        )
        nl.next_to(roots, DOWN, buff=2)
        self.play(
            derivEqualZero.animate.to_edge(UP)
        )
        always(roots.next_to, derivEqualZero, DOWN)

        self.play(
            ShowCreation(nl)
        )

        criticalDots = [Dot(color=RED), Dot(color=RED)]
        criticalDots[0].move_to(nl.n2p(x_criticals[0]))
        criticalDots[1].move_to(nl.n2p(x_criticals[1]))
        self.play(
            *[FadeIn(dot, scale=0.5) for dot in criticalDots]
        )

        """
        SCRIPT: tu cuc am den x = 1.766, ta biet dao ham ko doi dau
        """
        negToXminBrace = BraceBetweenPoints(nl.n2p(0), nl.n2p(x_criticals[0]), direction=UP)
        self.play(
            ShowCreation(negToXminBrace)
        )
        """
        SCRIPT" de xac dinh dau cua dao ham. lay x = 1, ta thay range f'(1) = 3.04 > 0
        """
        derivAtXEqual1 = Tex("f'(1) = 3.04 > 0")
        self.play(Write(derivAtXEqual1))
        """
        SCRIPT: dieu nay co nghia la dao ham > 0 trong vung nay, cung co nghia ham tang hoan toan 
        trong vung nay
        """
        negToXminBraceSignLabel = Tex("+")
        negToXminBraceSignLabel.next_to(negToXminBrace, UP)
        self.play(Write(negToXminBraceSignLabel))
        self.play(FadeOut(derivAtXEqual1))

        """
        SCRIPT: tu x= 1.766 den x= 5.xxx, 
        """
        xMinToxMaxBrace = BraceBetweenPoints(nl.n2p(x_criticals[0]), nl.n2p(x_criticals[1]), direction=UP)
        self.play(ShowCreation(xMinToxMaxBrace))
        """
        SCRIPT: do dao ham ko thay doi dau, ta tinh gia tri cua dao ham ta diem bat ki.
        """
        deriveAtXEqual3 = Tex("f'(3) = -2.68 < 0")
        self.play(Write(deriveAtXEqual3))
        """
        SCRIPT: ta thay range f'() < 0. , dieu nay co nghia la ham < 0 trong vung nay va ham
        giam hoan toan trong vung nay
        """
        xMinToxMaxBraceSignLabel = Tex("-")
        xMinToxMaxBraceSignLabel.next_to(xMinToxMaxBrace, UP)
        self.play(Write(xMinToxMaxBraceSignLabel))
        self.play(FadeOut(deriveAtXEqual3))

        """
        SCRIPT:
        Lam tuong tu voi x = 5.xxx toi cuc duong ta duong ket qua nhu sau
        """
        xMaxToPosInfBrace = BraceBetweenPoints(nl.n2p(x_criticals[1]), nl.n2p(7), direction=UP)
        xMaxToPosInfBraceSignLabel = Tex("+")
        xMaxToPosInfBraceSignLabel.next_to(xMaxToPosInfBrace, UP)
        self.play(ShowCreation(xMaxToPosInfBrace), Write(xMaxToPosInfBraceSignLabel))


        """
        SCRIPT: nhin vao bang bien thien ta thay
        """
        self.wait(1)
        """
        SCRIPT: do ham tang roi giam, 
        """
        self.play(ScaleInPlace(negToXminBraceSignLabel, 2, rate_func=there_and_back))
        self.play(ScaleInPlace(xMinToxMaxBraceSignLabel, 2, rate_func=there_and_back))

        """
        SCRIPT: diem nay la cuc dai
        """
        maxLabel = Text("Cực đại", font_size=30)
        maxLabel.next_to(criticalDots[0], UP, buff=2)
        maxArrow = Arrow(maxLabel, criticalDots[0])
        self.play(
            Write(maxLabel),
            Write(maxArrow),
            FadeIn(criticalDots[0], scale=0.2)
        )

        """
        SCRIPT: do ham giam roi tang, 
        """
        self.play(ScaleInPlace(xMinToxMaxBraceSignLabel, 2, rate_func=there_and_back))
        self.play(ScaleInPlace(xMaxToPosInfBraceSignLabel, 2, rate_func=there_and_back))
        """
        SCRIPT: diem nay la cuc tieu
        """
        maxLabel = Text("Cực tiểu", font_size=30)
        maxLabel.next_to(criticalDots[1], UP, buff=2)
        minArrow = Arrow(maxLabel, criticalDots[1])
        self.play(
            Write(maxLabel),
            Write(minArrow),
            FadeIn(criticalDots[1], scale=0.2)
        )


