<template>
  <v-container>
    <v-card class="mx-auto">
      <v-img src="/assets/Nextgen.png" cover></v-img>
      <v-card-title>
        GTAV中配模组
      </v-card-title>

      <v-card-subtitle>
        只在GTAMODX和3DM发布，禁止倒卖和未授权的转载
      </v-card-subtitle>

      <v-card-actions>
        <v-btn :icon="show ? 'mdi-chevron-up' : 'mdi-chevron-down'" @click="show = !show"></v-btn>

        <v-spacer></v-spacer>
        <v-btn color="blue" onclick="selectDirectory();" @click="resetDirectory()">
          选择目录
          <v-tooltip activator="parent" id="directory " location="top">选择游戏的安装目录</v-tooltip>
        </v-btn>
        <v-btn color="orange" onclick="install();" @click="resetProgress()">
          安装模组
          <v-tooltip activator="parent" id="directory " location="top">一键自动安装模组</v-tooltip>
        </v-btn>
        <v-btn color="orange-lighten-2" onclick="openGames()">
          启动游戏
          <v-tooltip activator="parent" location="top">Ciallo～(∠・ω< )⌒☆</v-tooltip>
        </v-btn>

      </v-card-actions>

      <v-slide-y-transition>
        <div v-if="isInstalling">
          <v-divider></v-divider>
          <v-card-text>
            <v-alert
              v-model="logAlert"
              border="start"
              variant="tonal"
              color="gray"
              class="log-container"
            >
              <pre>{{ latestLog }}</pre>
            </v-alert>
            <v-progress-linear
              v-if="progress < 100"
              v-model="progress"
              color="blue"
              height="10"
              striped
              rounded
              class="mb-4"
            >
              <template v-slot:default="{ value }">
                <strong>{{ Math.round(value) }}%</strong>
              </template>
            </v-progress-linear>
          </v-card-text>
        </div>
      </v-slide-y-transition>

      <v-expand-transition>
        <div v-show="show">
          <v-divider></v-divider>
          <v-card-text v-html="Info">
          </v-card-text>
        </div>
      </v-expand-transition>
    </v-card>

    <v-row id="Tomori">
      <v-col cols="12" sm="6" style="margin-top: 10px;">
        <v-card class="mx-auto pa-2" image="/assets/Bridge_view.png" subtitle="我们会公开鸣谢您的赞助，感谢您的支持！"
                title="赞助">
          <template v-slot:actions>
            <v-btn append-icon="mdi-chevron-right" color="red-lighten-2" text="爱发电主页" variant="outlined" block
                   @click="GameVideo"></v-btn>
          </template>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" style="margin-top: 10px;">
        <v-card class="mx-auto pa-2" image="/assets/Ocean_Drive.png" subtitle="关注作者Cyber蝈蝈总，获取最新动态"
                title="B站频道">
          <template v-slot:actions>
            <v-btn append-icon="mdi-chevron-right" color="red-lighten-2" text="作者主页" variant="outlined" block
                   @click="DownloadUrl"></v-btn>
          </template>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<style>
#Tomori .v-img__img--cover {
  opacity: 0.5;
}

.log-container pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0;
  font-family: monospace;
}

.v-progress-linear__content strong {
  color: white;
  text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.5);
  font-size: 0.6rem;
}
</style>
<script lang="ts">
declare function getInstallProgress(): Promise<number>;

declare function getLog(): Promise<string>;

export default {
  data: () => ({
    show: false,
    isInstalling: false,
    progress: 0,
    latestLog: "等待安装开始...",
    logAlert: true,
    updateInterval: null as number | null,
    Info: `
  <h1>GTAV中配</h1>
  <br>
  <p>作者：<a href="https://space.bilibili.com/37706580" target="_blank">B站-Cyber蝈蝈总</a>、<a href="https://mod.3dmgame.com/u/7715845" target="_blank">3DM-DJ小良</a></p>
  <br>
  <div style="background-color: #7B2257; padding: 10px; border: 1px solid #f5c6cb;">
      <strong>警告：</strong>
      <p><strong>该MOD免费，只在<a href="http://www.gtamodx.com" target="_blank">GTAMODX</a>和<a href="https://mod.3dmgame.com/" target="_blank">3DM</a>发布。</strong></p>
      <p><strong>禁止未授权的转载。禁止倒卖，用于盈利将承担相应责任！</strong></p>
  </div>
  <br>
  <h2>介绍</h2>
  <br>
  <p>国语配音制作流程：将字幕修改成适合用中国话自然说出来的形式，人工录制配音，部分角色使用AI将音色转为角色原本的音色。达到尽可能还原原作的效果。</p>
  <p><strong>增量迭代中！当前不是完整版！</strong></p>
  <br>
  <h2>制作人员</h2>
  <br>
  <ul>
      <li><strong>策划：</strong>Cyber蝈蝈总、DJ小良、小湿帝JokiJoki</li>
      <li><strong>字幕：</strong>Agera、阿笑-Seichi，CACOLAZY 、Cyber蝈蝈总、蓝风、tails、鸢鸣_Official、小湿帝JokiJoki、kagamiKILL、密申罗69号干员</li>
      <li><strong>配音：</strong>阿尔戈-Argo、阿笑-Seichi、CACOLAZY 、Cricket影音博物馆、Cyber蝈蝈总、Goldship、Hertz、进击的魔界人、小湿帝JokiJoki、蓝风、祈衍、鸢鸣_Official、崴脚小面包、封狼、Q、SCC、工新河、棒冰、九日草方、封狼、HA桑</li>
      <li><strong>测试/校对：</strong>志存高远之人、斐波那契数列参观者</li>
  </ul>
  <br>
  <h2>鸣谢</h2>
  <br>
  <ol>
      <li>鼠子</li>
      <li>徽信支付</li>
      <li>志存高远之人</li>
      <li>kagamiKILL</li>
      <li>銮为延器</li>
  </ol>
    `,
  }),
  methods: {
    DownloadUrl() {
      window.open('https://space.bilibili.com/37706580', '_blank');
    },
    GameVideo() {
      window.open('https://ifdian.net/a/Katock', '_blank');
    },
    startUpdateInterval() {
      this.updateInterval = setInterval(() => {
        getInstallProgress().then(progress => {
          this.progress = progress;
        });
        getLog().then(log => {
          this.latestLog = log;
        });
      }, 1000);
    },
    resetDirectory() {
      this.isInstalling = false;
    },
    resetProgress() {
      this.isInstalling = true;
      this.progress = 0;
      this.latestLog = "等待安装开始...";
    },
  },
  watch: {
    isInstalling(newVal) {
      if (newVal === true) {
        this.startUpdateInterval();
      } else if (this.updateInterval) {
        clearInterval(this.updateInterval);
        this.updateInterval = null;
      }
    },
  },
  beforeUnmount() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
    }
  }
}
</script>
