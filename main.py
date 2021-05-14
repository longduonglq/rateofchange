from manimlib import *
from math import *

class OpenScene(Scene):
    def construct(self):
        what_slope = Text("""Ý nghĩa của độ dốc tiếp tuyến?""")
        what_slope.to_edge(UP)
        what_derivative = Text("Của đạo hàm?")
        what_derivative.to_edge(UP)
        VGroup(what_slope, what_derivative).arrange(DOWN, buff=1)

        self.play(Write(what_slope))
        self.play(Write(what_derivative))
        self.wait(2)

        self.play(FadeOut(what_slope, UP),
                  FadeOut(what_derivative, DOWN))


class SlopeDiff(Scene):
    def construct(self):
        def func(x):
            return 5/(1+exp(-2.5*x+5)) + 5/(1+exp(-(2.5*x-19)))
            # return x**3 - 3.7*x**2 + 2*x + 2.6

        x_range = (0, 10)
        y_range = (0, 10)
        # instantaneous
        inst_axes = Axes(
            x_range, y_range,
            height=6,
            width=5
        )
        inst_axes.add_coordinate_labels()

        # avg
        avg_axes = Axes(
            x_range, y_range,
            height=6,
            width=5
        )
        avg_axes.add_coordinate_labels()

        axes_pair = VGroup(inst_axes, avg_axes)
        axes_pair.arrange(RIGHT, buff=MED_LARGE_BUFF)
        # axes_pair.to_corner(UL)

        inst_graph = inst_axes.get_graph(
            func,
            color=BLUE
        )
        inst_label = inst_axes.get_graph_label(
            inst_graph,
            "d(t)"
        )

        avg_graph = avg_axes.get_graph(
            func,
            color=BLUE
        )
        avg_label = avg_axes.get_graph_label(
            avg_graph,
            "d(t)"
        )

        # self.add(inst_axes, avg_axes)
        # animate
        self.play(
            Write(inst_axes, lag_ratio=0.01),
            Write(avg_axes, lag_ratio=0.01)
        )
        self.play(
            ShowCreation(inst_graph),
            FadeIn(inst_label, RIGHT),
            ShowCreation(avg_graph),
            FadeIn(avg_label, RIGHT)
        )

        # tangent line
        inst_dot = Dot(color=RED)
        inst_dot.move_to(inst_axes.i2gp(1, inst_graph))

        inst_tracker = ValueTracker(1)
        f_always(
            inst_dot.move_to,
            lambda: inst_axes.i2gp(inst_tracker.get_value(), inst_graph)
        )
        v_line = always_redraw(lambda: inst_axes.get_v_line(inst_dot.get_bottom()))

        tan_line = always_redraw(
            lambda:
            TangentLine(
                inst_graph,
                inst_tracker.get_value()/(x_range[1] - x_range[0]),
                length=2, stroke_capacity=0.75
            )
        )

        # slope =
        slope_text, slope_value = inst_slope_label = VGroup(
            Text("Độ dốc = ", font_size=26, font="Cambria"),
            DecimalNumber(
                0,
                show_ellipsis=False,
                num_decimal_places=1,
                include_sign=True,
                font_size=26
            )
        )
        inst_slope_label.arrange(RIGHT)
        always(inst_slope_label.next_to, inst_axes, UP)
        f_always(slope_value.set_value, tan_line.get_slope)

        self.play(Write(inst_slope_label))
        self.play(
            FadeIn(tan_line, scale=0.5),
            FadeIn(v_line, scale=0.5),
            FadeIn(inst_dot, scale=0.5)
        )

        self.play(inst_tracker.animate.set_value(10), run_time=5)
        self.play(inst_tracker.animate.set_value(4.5), run_time=5)
        self.wait()

        # SECANT
        sec_dots_value = [
            ValueTracker(1), ValueTracker(3)
        ]
        sec_dots = [Dot(color=RED), Dot(color=RED)]

        f_always(
            sec_dots[0].move_to,
            lambda: avg_axes.i2gp(sec_dots_value[0].get_value(), avg_graph)
        )
        f_always(
            sec_dots[1].move_to,
            lambda: avg_axes.i2gp(sec_dots_value[1].get_value(), avg_graph)
        )

        # sec_line = Line(
        #     avg_axes.i2gp(sec_dots_value[0].get_value(), avg_graph),
        #     avg_axes.i2gp(sec_dots_value[1].get_value(), avg_graph)
        # )
        # sec_line = always_redraw(
        #     Line,
        #     avg_axes.i2gp(sec_dots_value[0].get_value(), avg_graph),
        #     avg_axes.i2gp(sec_dots_value[1].get_value(), avg_graph)
        # )
        sec_line = always_redraw(
            lambda:
            Line(
                avg_axes.i2gp(sec_dots_value[0].get_value(), avg_graph),
                avg_axes.i2gp(sec_dots_value[1].get_value(), avg_graph)
            )
        )

        avg_slope_text, avg_slope_value = avg_slope_label = VGroup(
            Text("Độ dốc = ", font_size=26),
            DecimalNumber(
                0,
                show_ellipsis=False,
                num_decimal_places=1,
                include_sign=True,
                font_size=26
            )
        )
        avg_slope_label.arrange(RIGHT)
        always(avg_slope_label.next_to, avg_axes, UP)
        f_always(avg_slope_value.set_value, sec_line.get_slope)

        self.play(
            ShowCreation(sec_line),
            *(FadeIn(sd, scale=0.5) for sd in sec_dots),
            Write(avg_slope_label)
        )
        self.play(sec_dots_value[1].animate.set_value(8), run_time=2)
        self.play(sec_dots_value[0].animate.set_value(4), run_time=2)
        self.play(sec_dots_value[1].animate.set_value(5), run_time=2)

class MeaningOfDerivative(Scene):
    def construct(self):
        pass

class InstantaneousRateOfChange(Scene):
    def construct(self):
        def ideal_curve(x):
            return x

        def realistic_curve(x):
            return 9*exp(-0.5*(0.6*x - 3)**2)

        x_range = (0, 11)
        y_range = (0, 10)

        axes = Axes(x_range, y_range, height=6, width=5)
        axes.add_coordinate_labels()

        ideal_graph = axes.get_graph(ideal_curve, color=BLUE)
        real_graph = axes.get_graph(realistic_curve, color=BLUE)

        label = axes.get_graph_label(ideal_graph, "p(t)")

        self.play(Write(axes), Write(label))
        self.play(ShowCreation(ideal_graph, lag_ratio=0.01))
        self.wait()
        self.play(ReplacementTransform(ideal_graph, real_graph))

        # tangent line
        tracker_dot = Dot(color=RED)
        tracker_dot.move_to(axes.i2gp(0, real_graph))

        tracker = ValueTracker(0)
        f_always(
            tracker_dot.move_to,
            lambda : axes.i2gp(tracker.get_value(), real_graph)
        )
        vert_line = always_redraw(lambda: axes.get_v_line(tracker_dot.get_bottom()))

        tan_line = always_redraw(
            lambda:
            TangentLine(
                real_graph,
                tracker.get_value()/(x_range[1] - x_range[0]),
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

        self.play(tracker.animate.set_value(5), run_time=5)
        self.wait()
        self.play(tracker.animate.set_value(10), run_time=5)
        self.wait()

        self.play(tracker.animate.set_value(3), run_time=2)

        env_params = Text(
            """
            T = X °C \n

            Độ ẩm = X %
            """,
            font_size=25
        )
        env_params.next_to(axes, RIGHT_SIDE)
        self.play(Write(env_params))


        # bacteria
        bac_size = 0.2
        bac = SVGMobject(
            "bacteria.svg",
            height=bac_size
        )
        bac_lines = 1

        for i in range(0, 7):
            bac_lines += 2
            grid = bac.get_grid(bac_lines, bac_lines)
            grid.next_to(axes, LEFT)
            self.add(grid)
            self.wait(0.2)
            self.remove(grid)