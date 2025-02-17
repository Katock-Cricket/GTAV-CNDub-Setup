<template>
  <v-container>
    <v-card class="mx-auto">
      <v-img src="/assets/Nextgen.png" cover></v-img>
      <v-card-title>
        GTAV中配MOD安装器
      </v-card-title>

      <v-card-subtitle>
        只在GTAMODX和3DM发布，禁止倒卖和未授权的转载
      </v-card-subtitle>

      <v-card-actions>
        <v-btn :icon="show ? 'mdi-chevron-up' : 'mdi-chevron-down'" @click="show = !show"></v-btn>

        <v-spacer></v-spacer>
        <v-btn color="blue" onclick="selectDirectory()">
          选择目录
          <v-tooltip activator="parent" id="directory " location="top">选择游戏的安装目录</v-tooltip>
        </v-btn>
        <v-btn color="orange" onclick="install()" @click="isInstalled = true">
          安装模组
          <v-tooltip activator="parent" id="directory " location="top">一键自动安装模组</v-tooltip>
        </v-btn>
<!--        <v-btn color="red" onclick="uninstall()" @click="isInstalled = false" v-show="isInstalled">-->
<!--          卸载模组-->
<!--          <v-tooltip activator="parent" id="directory " location="top">一键自动卸载模组</v-tooltip>-->
<!--        </v-btn>-->
        <v-btn color="orange-lighten-2" onclick="openGames()">
          启动游戏
          <v-tooltip activator="parent" location="top">Ciallo～(∠・ω< )⌒☆</v-tooltip>
        </v-btn>

      </v-card-actions>

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
        <v-card class="mx-auto pa-2" image="/assets/Bridge_view.png" subtitle="我们会公开鸣谢您的赞助，感谢您的支持！" title="赞助">
          <template v-slot:actions>
            <v-btn append-icon="mdi-chevron-right" color="red-lighten-2" text="爱发电主页" variant="outlined" block
              @click="GameVideo"></v-btn>
          </template>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" style="margin-top: 10px;">
        <v-card class="mx-auto pa-2" image="/assets/Ocean_Drive.png" subtitle="关注作者Cyber蝈蝈总，获取最新动态" title="B站频道">
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
</style>
<script lang="ts">
export default {
  data: () => ({
    show: false,
    isInstalled: false,
    Info: `
  <h1>GTAV中配MOD</h1>
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
      <li><strong>字幕：</strong>Agera、阿笑-Seichi，CACOLAZY 、Cyber蝈蝈总、蓝风、tails、鸢鸣_Official、小湿帝JokiJoki</li>
      <li><strong>配音：</strong>阿尔戈-Argo、阿笑-Seichi、CACOLAZY 、Cricket影音博物馆、Cyber蝈蝈总、Goldship、Hertz、进击的魔界人、小湿帝JokiJoki、蓝风、祈衍、鸢鸣_Official、崴脚小面包、封狼、Q、SCC、工新河、棒冰、九日草方</li>
  </ul>
  <br>
  <p>制作组诚招感兴趣的老师或玩家参与配音和制作（非盈利项目）</p>
  <br>
  <h2>鸣谢</h2>
  <br>
  <ol>
      <li>鼠子（B站充电/GTAMODX充电）</li>
      <li>銮为延器（爱发电充电）</li>
  </ol>
    `,
  }),
  methods: {
    DownloadUrl() {
      window.open('https://space.bilibili.com/37706580', '_blank');
    },
    GameVideo() {
      window.open('https://ifdian.net/a/Katock', '_blank');
    }
  }
}
</script>
