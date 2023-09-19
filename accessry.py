class Accessory:

    def __init__(
            self,
            N_r,  # 精馏段塔板数
            N_s,  # 提馏段塔板数
            H_T=0.35,  # m 塔板间距
            H_bottom=1,  # m 最后一块板到塔底的距离
            H_top=0.7,  # m 第一块板到塔顶距离
            H_in=0.8,  # m 进料处板间距
            H_human=0.8,  # m 开人孔处间距
            H_heat=3,  # m 间接蒸汽加热裙座高度
            D_human=0.5,  # m 人孔直径
            N_human_dis=10,  # 块板 人孔间距
            human_start=4  # 人孔开始的层数
    ) -> None:
        self.N_r = N_r
        self.N_s = N_s
        self.N = N_r + N_s
        self.H_T = H_T
        self.H_bottom = H_bottom
        self.H_top = H_top
        self.H_in = H_in
        self.H_human = H_human
        self.H_heat = H_heat
        self.D_human = D_human
        self.N_human_dis = N_human_dis
        self.human_start = human_start

