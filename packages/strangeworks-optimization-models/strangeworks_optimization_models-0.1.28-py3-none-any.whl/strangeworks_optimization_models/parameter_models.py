from typing import List, Optional


class DwaveSamplerParameterModel:
    def __init__(
        self,
        num_reads: Optional[int] = 1,
        chain_strength: Optional[int] | None = None,
        anneal_offsets: Optional[List[float]] | None = None,
        anneal_schedule: Optional[List[List[float]]] | None = None,
        annealing_time: Optional[float] | None = None,
        auto_scale: Optional[bool] | None = None,
        flux_biases: Optional[List[float]] | None = None,
        flux_drift_compensation: Optional[bool] | None = None,
        h_gain_schedule: Optional[List[List[float]]] | None = None,
        initial_state: Optional[dict] | None = None,
        max_answers: Optional[int] | None = None,
        num_spin_reversal_transforms: Optional[int] | None = None,
        programming_thermalization: Optional[float] | None = None,
        readout_thermalization: Optional[float] | None = None,
        reduce_intersample_correlation: Optional[bool] | None = None,
        reinitialize_state: Optional[bool] | None = None,
    ) -> None:
        # See https://docs.dwavesys.com/docs/latest/c_solver_parameters.html
        # for details

        # Number of samples to run
        self.num_reads = num_reads
        # Weight of the links between qubits representig on variable
        self.chain_strength = chain_strength
        # Provides offsets to annealing paths, per qubit
        self.anneal_offsets = anneal_offsets
        # Introduces variations to the global anneal schedule.
        self.anneal_schedule = anneal_schedule
        # Sets the duration, in microseconds with a resolution of 0.01 𝜇𝑠
        # of quantum annealing time, per read
        self.annealing_time = annealing_time
        # Indicates whether ℎ and 𝐽 values are rescaled:
        self.auto_scale = auto_scale
        # List of flux-bias offset values with which to calibrate a chain.
        self.flux_biases = flux_biases
        # Boolean flag indicating whether the D-Wave system compensates for flux drift.
        self.flux_drift_compensation = flux_drift_compensation
        # Sets a time-dependent gain for linear coefficients (qubit biases, see the h parameter) in the Hamiltonian.
        self.h_gain_schedule = h_gain_schedule
        # Initial state to which the system is set for reverse annealing.
        self.initial_state = initial_state
        # Limits the returned values to the first max_answers of num_reads samples.
        self.max_answers = max_answers
        # Specifies the number of spin-reversal transforms to perform.
        self.num_spin_reversal_transforms = num_spin_reversal_transforms
        # Sets the time, in microseconds with a resolution of 0.01 𝜇𝑠,
        # to wait after programming the QPU for it to cool back to base
        # temperature (i.e., post-programming thermalization time).
        self.programming_thermalization = programming_thermalization
        # Sets the time, in microseconds with a resolution of 0.01 𝜇𝑠,
        # to wait after each state is read from the QPU for it to cool
        # back to base temperature (i.e., post-readout thermalization time).
        self.readout_thermalization = readout_thermalization
        # Reduces sample-to-sample correlations caused by the spin-bath polarization
        # effect by adding a delay between reads.
        self.reduce_intersample_correlation = reduce_intersample_correlation
        # When using the reverse annealing feature, you must supply the initial state
        # to which the system is set; see the initial_state parameter
        self.reinitialize_state = reinitialize_state


class DwaveLeapParameterModel:
    def __init__(
        self,
        time_limit: Optional[float] | None = None,
    ) -> None:
        # See https://docs.dwavesys.com/docs/latest/c_solver_parameters.html
        # for details

        # Specifies the maximum run time, in seconds, the solver is allowed to work on the given problem.
        self.time_limit = time_limit


class JijSAParameterModel:
    def __init__(
        self,
        feed_dict: Optional[dict] | None = None,
        num_search: Optional[int] = 1,
        multipliers: Optional[dict] | None = None,
        beta_min: float | None = None,
        beta_max: float | None = None,
        num_sweeps: int | None = None,
        num_reads: int | None = None,
        initial_state: list | dict | None = None,
        updater: str | None = None,
        sparse: bool | None = None,
        reinitialize_state: bool | None = None,
        seed: int | None = None,
        needs_square_constraints: dict[str, bool] | None = None,
        relax_as_penalties: dict[str, bool] | None = None,
    ) -> None:
        # See https://www.documentation.jijzept.com/docs/jijmodeling/
        # for details

        # Dictionary of coefficients for jm.Problem
        self.feed_dict = feed_dict
        # Number of times algorithm will be run
        self.num_search = num_search
        # Multipliers for any constraints in jm.Problem
        self.multipliers = multipliers
        # inverse temperature. If `None`, this will be set automatically.
        self.beta_min = beta_min
        # inverse temperature. If `None`, this will be set automatically.
        self.beta_max = beta_max
        #  The number of Monte-Carlo steps. If `None`, 1000 will be set.
        self.num_sweeps = num_sweeps
        #  The number of samples. If `None`, 1 will be set.
        self.num_reads = num_reads
        # Initial state. If `None`, this will be set automatically.
        self.initial_state = initial_state
        # Updater algorithm. "single spin flip" or "swendsen wang". If `None`, "single spin flip" will be set.
        self.updater = updater
        # If `True`, only non-zero matrix elements are stored, which will save memory. If `None`, `False` will be set.
        self.sparse = sparse
        # If `True`, reinitialize state for each run. If `None`, `True` will be set.
        self.reinitialize_state = reinitialize_state
        # Seed for Monte Carlo algorithm. If `None`, this will be set automatically.
        self.seed = seed
        # This dictionary object is utilized to determine whether to square the constraint condition while incorporating it into the QUBO/HUBO penalty term. Here, the constraint's name is used as the key. If the value is set to True, the corresponding constraint is squared upon its addition to the QUBO/HUBO penalty term. By default, the value is set to True for linear constraints, and to False for non-linear ones.
        self.needs_square_constraints = needs_square_constraints
        # This dictionary object is designed to regulate the incorporation of constraint conditions into the QUBO/HUBO penalty term, with the constraint's name functioning as the key. If the key's value is True, the respective constraint is added to the QUBO/HUBO penalty term. If the value is False, the constraint is excluded from the penalty term, though it remains subject to evaluation to verify if it meets the constraint conditions. By default, all constraint conditions have this value set to True.
        self.relax_as_penalties = relax_as_penalties


class JijSQAParameterModel:
    def __init__(
        self,
        feed_dict: Optional[dict] | None = None,
        num_search: Optional[int] = 1,
        multipliers: Optional[dict] | None = None,
        beta: float | None = None,
        gamma: float | None = None,
        trotter: int | None = None,
        num_sweeps: int | None = None,
        num_reads: int | None = None,
        sparse: bool | None = None,
        reinitialize_state: bool | None = None,
        seed: int | None = None,
        needs_square_constraints: dict[str, bool] | None = None,
        relax_as_penalties: dict[str, bool] | None = None,
    ) -> None:
        # See https://www.documentation.jijzept.com/docs/jijmodeling/
        # for details

        # Dictionary of coefficients for jm.Problem
        self.feed_dict = feed_dict
        # Number of times algorithm will be run
        self.num_search = num_search
        # Multipliers for any constraints in jm.Problem
        self.multipliers = multipliers
        # inverse temperature. If `None`, this will be set automatically.
        self.beta = beta
        # Strength of transverse field. this will be set automatically.
        self.gamma = gamma
        # The number of Trotter. this will be set automatically.
        self.trotter = trotter
        #  The number of Monte-Carlo steps. If `None`, 1000 will be set.
        self.num_sweeps = num_sweeps
        #  The number of samples. If `None`, 1 will be set.
        self.num_reads = num_reads
        # If `True`, only non-zero matrix elements are stored, which will save memory. If `None`, `False` will be set.
        self.sparse = sparse
        # If `True`, reinitialize state for each run. If `None`, `True` will be set.
        self.reinitialize_state = reinitialize_state
        # Seed for Monte Carlo algorithm. If `None`, this will be set automatically.
        self.seed = seed
        # This dictionary object is utilized to determine whether to square the constraint condition while incorporating it into the QUBO/HUBO penalty term. Here, the constraint's name is used as the key. If the value is set to True, the corresponding constraint is squared upon its addition to the QUBO/HUBO penalty term. By default, the value is set to True for linear constraints, and to False for non-linear ones.
        self.needs_square_constraints = needs_square_constraints
        # This dictionary object is designed to regulate the incorporation of constraint conditions into the QUBO/HUBO penalty term, with the constraint's name functioning as the key. If the key's value is True, the respective constraint is added to the QUBO/HUBO penalty term. If the value is False, the constraint is excluded from the penalty term, though it remains subject to evaluation to verify if it meets the constraint conditions. By default, all constraint conditions have this value set to True.
        self.relax_as_penalties = relax_as_penalties


class JijLeapHybridCQMParameterModel:
    def __init__(
        self,
        feed_dict: Optional[dict] | None = None,
        num_search: Optional[int] = 1,
        time_limit: int | float | None = None,
    ) -> None:
        # See https://www.documentation.jijzept.com/docs/jijmodeling/
        # for details

        # Dictionary of coefficients for jm.Problem
        self.feed_dict = feed_dict
        # Number of times algorithm will be run
        self.num_search = num_search
        # The maximum run time
        self.time_limit = time_limit


class AquilaParameterModel:
    def __init__(
        self,
        unit_disk_radius: float,
        shots: Optional[int] = 100,
    ) -> None:
        # Radius of interactions for specified graph
        self.unit_disk_radius = unit_disk_radius
        # Number of times experiemnt will be run and qubits will be measured
        self.shots = shots


class NECParameterModel:
    def __init__(
        self,
        offset: Optional[float] = 0.0,
        num_reads: Optional[int] | None = None,
        num_results: Optional[int] | None = None,
        num_sweeps: Optional[int] | None = None,
        beta_range: Optional[List[float]] | None = None,
        beta_list: Optional[List[float]] | None = None,
        dense: Optional[bool] | None = None,
        vector_mode: Optional[str] | None = None,
        timeout: Optional[List[List[float]]] | None = None,
        Ve_num: Optional[int] | None = None,
        onehot: Optional[int] | None = None,
        fixed: Optional[list] | Optional[dict] | None = None,
        andzero: Optional[list] | None = None,
        orone: Optional[list] | None = None,
        supplement: Optional[list] | None = None,
        maxone: Optional[list] | None = None,
        minmaxone: Optional[list] | None = None,
        init_spin: Optional[list] | None = None,
        spin_list: Optional[list] | None = None,
    ) -> None:
        # Offset for the normalized weight information stored in the qubo
        self.offset = offset
        # VA sampling rate
        self.num_reads = num_reads
        # Number of VA annealing results
        self.num_results = num_results
        # Number of VA annealing sweeps
        self.num_sweeps = num_sweeps
        # VA beta value [start, end, steps] format
        self.beta_range = beta_range
        # Beta value array for each VA sweep
        self.beta_list = beta_list
        # VA matrix mode
        self.dense = dense
        # Mode during VA annealing
        self.vector_mode = vector_mode
        # Job execution timeout
        self.timeout = timeout
        # Number of VEs used in VA annealing
        self.Ve_num = Ve_num
        # VA onehot constraint parameter
        self.onehot = onehot
        # VA fixed constraint parameter
        self.fixed = fixed
        # VA andzero constraint parameter
        self.andzero = andzero
        # VA orone constraint parameter
        self.orone = orone
        # VA supplement constraint parameter
        self.supplement = supplement
        # VA maxone constraint parameter
        self.maxone = maxone
        # VA minmaxone constraint parameter
        self.minmaxone = minmaxone
        # VA initial spin parameter
        self.init_spin = init_spin
        # VA spin list parameter
        self.spin_list = spin_list


class QuantagoniaParameterModel:
    def __init__(
        self,
        sense: Optional[str] = "MINIMIZE",
        timelimit: Optional[float] = 86400,
        relative_gap: Optional[float] = 1e-4,
        absolute_gap: Optional[float] = 1e-9,
        # the following options only affect QUBOs, for MIPs they are ignored
        heuristics_only: Optional[bool] = False,
    ) -> None:
        # Type of cost function: MINIMIZE or MAXIMIZE
        self.sense = sense
        self.timelimit = timelimit
        self.relative_gap = relative_gap
        self.absolute_gap = absolute_gap
        # the following options only affect QUBOs, for MIPs they are ignored
        self.heuristics_only = heuristics_only


class GurobiParameterModel:
    def __init__(
        self,
        max_seconds: Optional[int] | None = None,
    ) -> None:
        # Maximum runtime for problem
        self.max_seconds = max_seconds

        # TODO: Add more parameters: https://www.gurobi.com/documentation/10.0/refman/parameters.html#sec:Parameters  # noqa


class ToshibaParameterModel:
    def __init__(
        self,
        algo: Optional[str] = "2.0",
        steps: Optional[int] | None = None,
        loops: Optional[int] | None = None,
        timeout: Optional[int] | None = None,
        target: Optional[float] | None = None,
        maxout: Optional[int] | None = None,
        dt: Optional[float] | None = None,
        C: Optional[float] | None = None,
        auto: Optional[bool] | None = None,
    ) -> None:
        # For details: https://learn.microsoft.com/en-us/azure/quantum/provider-toshiba

        # Specifies the type of SQBM+ computation algorithm.
        self.algo = algo
        # Specifies the number of steps in a computation request.
        self.steps = steps
        # Specifies the number of loops in SQBM+ computation.
        self.loops = loops
        # Specifies the maximum computation time (timeout) in seconds.
        self.timeout = timeout
        # Specifies the end condition of a computation request.
        self.target = target
        # Specifies the upper limit of the number of solutions to be outputted.
        self.maxout = maxout
        # Specifies the time per step.
        self.dt = dt
        # Corresponds to the constant ξ0, appearing in the paper by Goto,
        # Tatsumura, & Dixon (2019, p. 2), which is the theoretical basis of SQBM+.
        self.C = C
        # 	Specifies the parameter auto tuning flag.
        self.auto = auto


class HitachiParameterModel:
    """
    Default parameters:
        type: Optional[int] = None,
        num_executions: Optional[int] = 1,
        temperature_num_steps: Optional[int] = 10,
        temperature_step_length: Optional[int] = 100,
        temperature_initial: Optional[float] = 10.0,
        temperature_target: Optional[float] = 0.01,
        energies: Optional[bool] = True,
        spins: Optional[bool] = True,
        execution_time: Optional[bool] = False,
        num_outputs: Optional[int] = 0,
        averaged_spins: Optional[bool] = False,
        averaged_energy: Optional[bool] = False,
    """

    def __init__(
        self,
        solver_type: int | None = None,
        num_executions: int | None = None,
        temperature_num_steps: int | None = None,
        temperature_step_length: int | None = None,
        temperature_initial: float | None = None,
        temperature_target: float | None = None,
        energies: bool | None = None,
        spins: bool | None = None,
        execution_time: bool | None = None,
        num_outputs: int | None = None,
        averaged_spins: bool | None = None,
        averaged_energy: bool | None = None,
    ) -> None:
        self.solver_type = solver_type
        self.num_executions = num_executions
        self.temperature_num_steps = temperature_num_steps
        self.temperature_step_length = temperature_step_length
        self.temperature_initial = temperature_initial
        self.temperature_target = temperature_target
        self.energies = energies
        self.spins = spins
        self.execution_time = execution_time
        self.num_outputs = num_outputs
        self.averaged_spins = averaged_spins
        self.averaged_energy = averaged_energy

    def get_hitachi_api_parameters(self) -> dict:
        return {
            k: v
            for k, v in {
                "temperature_num_steps": self.temperature_num_steps,
                "temperature_step_length": self.temperature_step_length,
                "temperature_initial": self.temperature_initial,
                "temperature_target": self.temperature_target,
            }.items()
            if v is not None
        }

    def get_hitachi_api_output(self) -> dict:
        return {
            k: v
            for k, v in {
                "energies": self.energies,
                "spins": self.spins,
                "execution_time": self.execution_time,
                "num_outputs": self.num_outputs,
                "averaged_spins": self.averaged_spins,
                "averaged_energy": self.averaged_energy,
            }.items()
            if v is not None
        }


class FujitsuParameterModel:
    def __init__(
        self,
        time_limit_sec: int | None = None,
        target_energy: float | None = None,
        num_run: int | None = None,
        num_group: int | None = None,
        num_output_solution: int | None = None,
        gs_level: int | None = None,
        gs_cutoff: int | None = None,
        one_hot_level: int | None = None,
        one_hot_cutoff: int | None = None,
        internal_penalty: int | None = None,
        penalty_auto_mode: int | None = None,
        penalty_coef: int | None = None,
        penalty_inc_rate: int | None = None,
        max_penalty_coef: int | None = None,
        guidance_config: dict | None = None,
        fixed_config: dict | None = None,
        one_way_one_hot_groups: dict | None = None,
        two_way_one_hot_groups: dict | None = None,
    ) -> None:
        #  For details: https://portal.aispf.global.fujitsu.com/apidoc/da/jp/api-ref/da-qubo-v3c-en.html#/v3c

        # Maximum running time of DA in seconds (int64 type)
        # Specifies the upper limit of running time. The unit is seconds.
        # The calculation is terminated when the running time reaches the upper limit time specified by time_limit_sec.
        # Specifies an integer from 1 to 3600. (Default: 10)
        self.time_limit_sec = time_limit_sec

        # Threshold energy for fast exit (double type)
        # Specifies the target energy value. If not specified, the calculation will be performed without setting the target energy value.
        # When the minimum energy value reaches the target energy value, the calculation is terminated even if the running time does not reach the upper limit time.
        # Specifies a value from -2126 to 2126. (Default: disabled)
        self.target_energy = target_energy

        # The number of parallel attempts of each groups (int64 type)
        # num_run x num_group specifies the number of parallel attempts.
        # Specifies an integer from 1 to 1024. (Default: 16)
        self.num_run = num_run

        # The number of groups of parallel attempts (int64 type)
        # num_run x num_group specifies the number of parallel attempts.
        # Specifies an integer from 1 to 16. (Default: 1)
        self.num_group = num_group

        # The number of output solutions of each groups (int64 type)
        # num_output_solution x num_group specifies the number of output solutions.
        # Specifies an integer from 1 to 1024. (Default: 5)
        self.num_output_solution = num_output_solution

        # Level of the global search (int64 type)
        # In the global search, the search starting point with local solution group escape is determined, and the constrained search combining various search methods is repeatedly executed as a processing unit. The higher the value, the longer the constraint exploitation search.
        # Specifies the level of the global search. Lower level is weak on Global Search.
        # If you specify one-way one-hot constraints (one_way_one_hot_groups) or two-way one-hot constraints (two_way_one_hot_groups), it is recommended to specify 0 for gs_level.
        # Specifies an integer from 0 to 100. (Default: 5)
        self.gs_level = gs_level

        # Global search cutoff level (int64 type)
        # Specifies the convergence judgment level for global search constraint usage search. The higher the value, the longer the period during which the constraint-based search energy on which convergence is based is not updated. Convergence assessment is turned off at 0.
        # Specifies an integer from 0 to 1000000. (Default: 8000)
        self.gs_cutoff = gs_cutoff

        # Level of the 1hot constraint search (int64 type)
        # Specifies the level of 1hot constraint search, which is one of the constraint exploitation searches. The higher the value, the longer the 1hot constraint search.
        # Specifies an integer from 0 to 100. (Default: 3)
        self.one_hot_level = one_hot_level

        # Level of the convergence for 1hot constraint search (int64 type)
        # Specifies the convergence level for 1hot constraint search, one of the constraint exploitation searches. The higher the value, the longer the non-renewal period of the energy used as a reference for the convergence determination in the 1hot constraint search. Convergence assessment is turned off at 0.
        # Specifies an integer from 0 to 1000000. (Default: 100)
        self.one_hot_cutoff = one_hot_cutoff

        # Mode of 1hot constraint internal generation (int64 type)
        # Specifies the 1hot constraint internal generation mode. 0 turns off 1hot constrained internal generation mode.
        # Specifies an integer 0 or 1. (Default: 0)
        # If 1way 1hot constraint (one_way_one_hot_groups) or a 2way 1hot constraint (two_way_one_hot_groups) is specified, it is recommended that 1 be specified for internal_penalty.
        # If internal_penalty is not specified, or if internal_penalty is specified as 0, then the BinaryPolynomial or PenaltyBinaryPolynomial for the combinatorial optimization problem must be a quadratic polynomial indicating a condition for the 1way 1hot constraint (one_way_one_hot_groups) or the 2way 1hot constraint (two_way_one_hot_groups).
        # If internal_penalty is 1, the BinaryPolynomial or PenaltyBinaryPolynomial for the combinatorial optimization problem need not be a quadratic polynomial indicating the condition of the 1way 1hot constraint (one_way_one_hot_groups) or the 2way 1hot constraint (two_way_one_hot_groups).
        # If 1way 1hot constraint (one_way_one_hot_groups) is specified, the variable with the lowest variable number must be specified as a quadratic polynomial even if the coefficient is 0.
        # If 2way 1hot constraint (two_way_one_hot_groups) is specified, all diagonal terms must be specified as quadratic polynomials even if the coefficient is 0.
        # 　Specification example: When the number of variables is 4.
        # 　　　　　"binary_polynomial":
        # 　　　　　　{ "terms":[
        # 　　　　　　　{ "p": [0, 0], "c": 0 },
        # 　　　　　　　{ "p": [1, 1], "c": 0 },
        # 　　　　　　　{ "p": [2, 2], "c": 0 },
        # 　　　　　　　{ "p": [3, 3], "c": 0 }] }
        self.internal_penalty = internal_penalty

        # Coefficient adjustment mode (int64 type)
        # Specifies the coefficient adjustment mode for constraint terms.
        # 0: behavior with fixed value specified by penalty_coef
        # 1-10000: internally autofit with penalty_coef as initial value
        # Specifies an integer from 0 to 10000. (Default: 1)
        self.penalty_auto_mode = penalty_auto_mode

        # Coefficient of the constraint term (int64 type)
        # Specifies the coefficient of the constraint term.
        # Specifies an integer from 1 to 9223372036854775807. (Default: 1)
        self.penalty_coef = penalty_coef

        # Parameters for automatic adjustment of constraint terms (int64 type)
        # Specifies the parameter for automatic adjustment of the constraint term in the global search.
        # Specifies an integer from 100 to 200. (Default: 150)
        self.penalty_inc_rate = penalty_inc_rate

        # Maximum constraint term coefficent (int64 type)
        # Specifies the maximum constraint term coefficent. Set to 0 for no maximum value.
        # Specifies an integer from 0 to 9223372036854775807. (Default: 0)
        self.max_penalty_coef = max_penalty_coef

        # {
        # description:
        # Initial value of each variable ("uint32 type":boolean type)

        # Specifies an initial value for each polynomial (problem) variable that is set to find an optimal solution.
        # By specifying a value that is close to the optimal solution, improvement in the accuracy of the optimal solution can be expected.

        # Specifies an initial value for each of the variables with the following format:
        # 　Format: {"VariableNumber":InitialValue, "VariableNumber":InitialValue, ...}
        # 　Specification example: When you specify an initial value for each variable of 2x1x2 - 4x2x4
        # 　　　　　{"1":false,"2":false,"4":false}

        # If you do not specify initial values, the solver sets values randomly.

        # integer($uint32)	boolean
        # }
        self.guidance_config = guidance_config

        # {
        # description:
        # Fixed value of each variable ("uint32 type":boolean type)

        # Specifies a fixed value for each polynomial (problem) variable that is set to find an optimal solution.
        # The specified variable is fixed at the specified value.
        # However, if fixing at the specified value does not result in the optimal solution, it may not be fixed at the specified value.

        # Specifies a fixed value for each of the variables with the following format:
        # 　Format: {"VariableNumber":FixedValue, "VariableNumber":FixedValue, ...}
        # 　Specification example: When fixed values (false) are specified for variables x1, x2, and x4 of 2x1x2 - 4x2x4 + 7x3x5
        # 　　　　　{"1":false,"2":false,"4":false}

        # Variables that are not specified are not fixed.

        # integer($uint32)	boolean
        # }
        self.fixed_config = fixed_config

        # {
        # description:
        # Specifies the number of variables in each group of one-way one-hot constraints.
        # When one_way_one_hot_groups is specified, search for the solution with one "True" value among the variables in the same group.
        # If internal_penalty is not specified, or if internal_penalty is specified as 0, then the BinaryPolynomial or PenaltyBinaryPolynomial for the combinatorial optimization problem must be a quadratic polynomial indicating a condition for the 1way 1hot constraint (one_way_one_hot_groups). The "numbers" has an array of the number of variables in the same group.
        # The starting index is the minimum variable number of the combinatorial optimization problem specified for the binary polynomial (BinaryPolynomial) or the penalty binary polynomial (PenaltyBinaryPolynomial).
        # If you specify one_way_one_hot_groups, it is recommended to create a combinatorial optimization problem with consecutive variable numbers.

        # Specifies the number of variables in each group in the following format:
        # Format: {"numbers": [Number of variables in group 1, Number of variables in group 2, ...]}
        # Specification example: When grouping variable numbers 0 to 11 into [0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11] (Constraints that only one "True" value among the variable in each groups)
        # 　　　　　{"numbers": [4, 3, 5]}

        # numbers	[...]
        # }
        self.one_way_one_hot_groups = one_way_one_hot_groups

        # {
        # description:
        # Specifies the number of variables in each group of two-way one-hot constraints.
        # When two_way_one_hot_groups is specified, search for the solution with one "True" value among the columns and rows of square consisting of variables of rows and columns in the same group.
        # If internal_penalty is not specified, or if internal_penalty is specified as 0, then the BinaryPolynomial or PenaltyBinaryPolynomial for the combinatorial optimization problem must be a quadratic polynomial indicating a condition for the 2way 1hot constraint (two_way_one_hot_groups). The "numbers" has an array of the number of variables in the same group. Values in the numbers array must be the squared number.
        # The starting index is the minimum variable number of the combinatorial optimization problem specified for the binary polynomial (BinaryPolynomial) or the penalty binary polynomial (PenaltyBinaryPolynomial).
        # If you specify two_way_one_hot_groups, it is recommended to create a combinatorial optimization problem with consecutive variable numbers.

        # Specifies the number of variables in each group in the following format:
        # 　Format: {"numbers": [Number of variables in group 1, Number of variables in group 2, ...]}
        # 　Specification example: Specifies 16 for a 4x4 group, 25 for a 5x5 group, and 36 for a 6x6 group.
        # 　　　　　{"numbers": [16, 25, 36]}

        # numbers	[...]
        # }
        self.two_way_one_hot_groups = two_way_one_hot_groups
