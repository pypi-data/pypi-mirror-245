#include <pinocchio/fwd.hpp>

#include "expose-utils.hpp"
#include "module.h"
#include "registry.h"
#include "placo/humanoid/walk_pattern_generator.h"
#include "placo/kinematics/kinematics_solver.h"
#include "placo/humanoid/footsteps_planner.h"
#include "placo/humanoid/swing_foot.h"
#include "placo/humanoid/swing_foot_quintic.h"
#include "placo/humanoid/swing_foot_cubic.h"
#include "placo/humanoid/walk_tasks.h"
#include "placo/humanoid/lipm.h"
#include <Eigen/Dense>
#include <boost/python.hpp>

using namespace placo;
using namespace boost::python;
using namespace placo::kinematics;
using namespace placo::humanoid;

void exposeWalkPatternGenerator()
{
  class__<WalkPatternGenerator::Trajectory>("WalkTrajectory")
      .add_property("t_start", &WalkPatternGenerator::Trajectory::t_start)
      .add_property("t_end", &WalkPatternGenerator::Trajectory::t_end)
      .add_property("jerk_planner_timesteps", &WalkPatternGenerator::Trajectory::jerk_planner_timesteps)
      .def("get_T_world_left", &WalkPatternGenerator::Trajectory::get_T_world_left)
      .def("get_supports", &WalkPatternGenerator::Trajectory::get_supports)
      .def("get_T_world_right", &WalkPatternGenerator::Trajectory::get_T_world_right)
      .def("get_p_world_CoM", &WalkPatternGenerator::Trajectory::get_p_world_CoM)
      .def("get_v_world_CoM", &WalkPatternGenerator::Trajectory::get_v_world_CoM)
      .def("get_a_world_CoM", &WalkPatternGenerator::Trajectory::get_a_world_CoM)
      .def("get_j_world_CoM", &WalkPatternGenerator::Trajectory::get_j_world_CoM)
      .def("get_p_world_ZMP", &WalkPatternGenerator::Trajectory::get_p_world_ZMP)
      .def("get_p_world_DCM", &WalkPatternGenerator::Trajectory::get_p_world_DCM)
      .def("get_R_world_trunk", &WalkPatternGenerator::Trajectory::get_R_world_trunk)
      .def("support_side", &WalkPatternGenerator::Trajectory::support_side)
      .def("support_is_both", &WalkPatternGenerator::Trajectory::support_is_both)
      .def("get_support", &WalkPatternGenerator::Trajectory::get_support)
      .def("get_next_support", &WalkPatternGenerator::Trajectory::get_next_support)
      .def("get_prev_support", &WalkPatternGenerator::Trajectory::get_prev_support)
      .def("get_part_t_start", &WalkPatternGenerator::Trajectory::get_part_t_start)
      .def("apply_transform", &WalkPatternGenerator::Trajectory::apply_transform);

  class__<WalkPatternGenerator>("WalkPatternGenerator", init<HumanoidRobot&, HumanoidParameters&>())
      .def("plan", &WalkPatternGenerator::plan)
      .def("replan", &WalkPatternGenerator::replan)
      .def("can_replan_supports", &WalkPatternGenerator::can_replan_supports)
      .def("replan_supports", &WalkPatternGenerator::replan_supports);

  class__<SwingFoot>("SwingFoot", init<>())
      .def("make_trajectory", &SwingFoot::make_trajectory)
      .def("remake_trajectory", &SwingFoot::remake_trajectory);

  class__<SwingFootCubic::Trajectory>("SwingFootCubicTrajectory", init<>())
      .def("pos", &SwingFootCubic::Trajectory::pos)
      .def("vel", &SwingFootCubic::Trajectory::vel);

  class__<SwingFootCubic>("SwingFootCubic", init<>()).def("make_trajectory", &SwingFootCubic::make_trajectory);

  class__<SwingFoot::Trajectory>("SwingFootTrajectory", init<>())
      .def("pos", &SwingFoot::Trajectory::pos)
      .def("vel", &SwingFoot::Trajectory::vel);

  class__<SwingFootQuintic>("SwingFootQuintic", init<>()).def("make_trajectory", &SwingFootQuintic::make_trajectory);

  class__<SwingFootQuintic::Trajectory>("SwingFootQuinticTrajectory", init<>())
      .def("pos", &SwingFootQuintic::Trajectory::pos)
      .def("vel", &SwingFootQuintic::Trajectory::vel);

  class__<WalkTasks>("WalkTasks", init<>())
      .def(
          "initialize_tasks", +[](WalkTasks& tasks, KinematicsSolver& solver,
                                  HumanoidRobot& robot) { tasks.initialize_tasks(&solver, &robot); })
      .def(
          "update_tasks_from_trajectory", +[](WalkTasks& tasks, WalkPatternGenerator::Trajectory& trajectory,
                                              double t) { return tasks.update_tasks(trajectory, t); })
      .def(
          "update_tasks",
          +[](WalkTasks& tasks, Eigen::Affine3d T_world_left, Eigen::Affine3d T_world_right, Eigen::Vector3d com_world,
              Eigen::Matrix3d R_world_trunk) {
            return tasks.update_tasks(T_world_left, T_world_right, com_world, R_world_trunk);
          })
      .def(
          "reach_initial_pose",
          +[](WalkTasks& tasks, Eigen::Affine3d T_world_left, double feet_spacing, double com_height,
              double trunk_pitch) {
            return tasks.reach_initial_pose(T_world_left, feet_spacing, com_height, trunk_pitch);
          })
      .def("remove_tasks", &WalkTasks::remove_tasks)
      .def(
          "get_tasks_error",
          +[](WalkTasks& tasks) {
            auto errors = tasks.get_tasks_error();
            boost::python::dict dict;
            for (auto key : errors)
            {
              dict[key.first + "_x"] = key.second[0];
              dict[key.first + "_y"] = key.second[1];
              dict[key.first + "_z"] = key.second[2];
            }
            return dict;
          })
      .add_property(
          "solver", +[](WalkTasks& tasks) { return *tasks.solver; })
      .add_property("scaled", &WalkTasks::scaled, &WalkTasks::scaled)
      .add_property("left_foot_task", &WalkTasks::left_foot_task)
      .add_property("right_foot_task", &WalkTasks::right_foot_task)
      .add_property("trunk_mode", &WalkTasks::trunk_mode, &WalkTasks::trunk_mode)
      .add_property("com_x", &WalkTasks::com_x, &WalkTasks::com_x)
      .add_property("com_y", &WalkTasks::com_y, &WalkTasks::com_y)
      .add_property(
          "trunk_orientation_task", +[](WalkTasks& tasks) { return *tasks.trunk_orientation_task; });

  class__<LIPM::Trajectory>("LIPMTrajectory", init<>())
      .def("pos", &LIPM::Trajectory::pos)
      .def("vel", &LIPM::Trajectory::vel)
      .def("acc", &LIPM::Trajectory::acc)
      .def("jerk", &LIPM::Trajectory::jerk)
      .def("zmp", &LIPM::Trajectory::zmp)
      .def("dzmp", &LIPM::Trajectory::dzmp)
      .def("dcm", &LIPM::Trajectory::dcm);

  class__<LIPM>("LIPM", init<problem::Problem&, int, double, Eigen::Vector2d, Eigen::Vector2d, Eigen::Vector2d>())
      .def("pos", &LIPM::pos)
      .def("vel", &LIPM::vel)
      .def("acc", &LIPM::acc)
      .def("jerk", &LIPM::jerk)
      .def("zmp", &LIPM::zmp)
      .def("dzmp", &LIPM::dzmp)
      .def("dcm", &LIPM::dcm)
      .def("compute_omega", &LIPM::compute_omega)
      .def("get_trajectory", &LIPM::get_trajectory)
      .add_property("x", &LIPM::x)
      .add_property("y", &LIPM::y);
}