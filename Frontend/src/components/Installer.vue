<template>
  <v-container>
    <v-card class="mx-auto">
      <v-img src="/assets/Nextgen.png" cover></v-img>
      <v-card-title>
        GTAV中配模组-正式版v1.0
      </v-card-title>

      <v-card-subtitle>
        只在GTAMODX和3DM发布，禁止倒卖和未授权的转载
      </v-card-subtitle>

      <v-slide-y-transition>
        <div v-if="isInstalling">
          <v-divider></v-divider>
          <v-card-text>
            <v-alert v-model="logAlert" border="start" variant="tonal" color="gray" class="log-container">
              <pre>{{ latestLog }}</pre>
            </v-alert>
            <v-progress-linear v-if="progress < 100" v-model="progress" color="blue" height="10" striped rounded
              class="mb-4">
              <template v-slot:default="{ value }">
                <strong>{{ Math.round(value) }}%</strong>
              </template>
            </v-progress-linear>
          </v-card-text>
        </div>
      </v-slide-y-transition>

      <v-card-actions>
        <v-btn @click="showInfo = !showInfo">
          说明书
          <v-icon v-if="showInfo">mdi-chevron-up</v-icon>
          <v-icon v-else>mdi-chevron-down</v-icon>
        </v-btn>
        <v-select v-model="selectedModules" :items="modules" :item-props="itemProps" item-title="name" label="安装配音内容"
          chips multiple density="compact" max-width="600px" class="select-container"></v-select>
        <v-spacer></v-spacer>

        <v-btn color="blue" onclick="selectDirectory();" @click="resetDirectory()">
          选择游戏位置
          <v-tooltip activator="parent" id="directory " location="top">GTA5.exe或GTA5_enhanced.exe所在文件夹</v-tooltip>
        </v-btn>
        <v-btn color="orange" onclick="install();" @click="resetProgress()">
          安装模组
          <v-tooltip activator="parent" id="install " location="top">一键自动安装所选配音内容</v-tooltip>
        </v-btn>
        <v-btn color="red" @click="uninstallDialog = true">
          卸载模组
          <v-tooltip activator="parent" id="uninstall " location="top">自动卸载中配模组</v-tooltip>
        </v-btn>

      </v-card-actions>

      <!--      是否确定卸载的对话框-->
      <v-dialog v-model="uninstallDialog" width="700px">
        <v-card>
          <v-card-title>
            <span class="headline">确定要卸载模组吗？</span>
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <p>
                  注意：此操作将直接删除mods文件夹中所有包含中配的RPF文件，如果您有其他模组安装在这些RPF中也会被删除！ </p>
                <p>如果存在以上情况，建议您使用OpenIV或其他工具进行手动卸载。</p>
                <p>dinput8.dll、dsound.dll、OpenIV.asi、OpenRPF.asi等文件是mod加载器，请酌情手动删除。</p>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="red" onclick="uninstall();" @click="uninstallDialog = false; isInstalling = true;">确认卸载
            </v-btn>
            <v-btn color="blue" @click="uninstallDialog = false">取消</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>


      <v-expand-transition>
        <div v-show="showInfo">
          <v-divider></v-divider>
          <v-card-text v-html="Info" class="markdown-body" style="font-size: small" />
        </div>
      </v-expand-transition>
    </v-card>

    <v-row id="Tomori">
      <v-col cols="12" sm="6" style="margin-top: 10px;">
        <v-card class="mx-auto pa-2" image="/assets/Bridge_view.png" subtitle="欢迎访问GTAV中配MOD官方网站" title="官网">
          <template v-slot:actions>
            <v-btn append-icon="mdi-chevron-right" color="red-lighten-2" text="官方网站" variant="outlined" block
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

.markdown-body {
  margin: 0 auto;
}

@media (max-width: 1000px) {
  .markdown-body {
    padding: 15px;
  }
}

.select-container {
  margin-top: 20px;
}
</style>
<script lang="ts">
import MarkdownIt from 'markdown-it'
import { ref } from 'vue';
import 'github-markdown-css';


declare function getInstallProgress(): Promise<number>;

declare function getLog(): Promise<string>;

declare function updateModules(selectedModules: string[]): any;

export default {
  data: () => ({
    showInfo: false,
    isInstalling: false,
    progress: 0,
    latestLog: "等待安装开始...",
    logAlert: true,
    updateInterval: null as number | null,
    Info: ref(''),
    modules: [{
      name: '主角配音',
      tip: '[必选]真人配音，常见角色包括三主角在大世界中的触发式语音'
    },
    {
      name: '剧情配音',
      tip: '[必选]真人配音，部分前期剧情任务的语音、大世界事件'
    },
    {
      name: '周边汉化',
      tip: '[必选]真人配音，部分电视节目；启动动画；部分剧情涉及的贴图汉化'
    },
    {
      name: '配套字幕',
      tip: '[推荐]剧情任务配音的定制字幕，增强版安装此项会导致乱码'
    },
    {
      name: 'NPC配音',
      tip: '[可选]AI配音，覆盖几乎所有路人NPC的语音(7万+条)，质量一般'
    }],
    selectedModules: [''],
    uninstallDialog: false,
  }),
  async created() {
    try {
      let md = new MarkdownIt();
      let response = await fetch('/assets/GTA5中配MOD说明书.md');
      let text = await response.text();
      this.Info = md.render(text); //传入文本
      // 将info中的<a href替换为<a target="_blank" href，以便在新窗口打开
      this.Info = this.Info.replace(/<a href/g, '<a target="_blank" href');
      console.log('加载 markdown 文件成功:', this.Info);
    } catch (error) {
      console.error('加载 markdown 文件失败:', error);
      this.Info = '<p>加载信息失败，请检查说明文档是否存在</p>';
    }
  },
  beforeMount() {
    this.selectedModules = this.modules.map((item: any) => item.name);
  },
  methods: {
    itemProps(item: { name: string, tip: string }) {
      return {
        title: item.name,
        subtitle: item.tip,
      }
    },
    DownloadUrl() {
      window.open('https://space.bilibili.com/37706580', '_blank');
    },
    GameVideo() {
      window.open('https://v-cn.gtamodx.com/', '_blank');
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
      this.latestLog = "等待操作开始...";
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
    selectedModules: {
      handler(newVal: any) {
        // 如果必选项未选中，则自动加在前面
        let frozenModules = this.modules.filter(item =>
          item.name === '主角配音' ||
          item.name === '剧情配音' ||
          item.name === '周边汉化'
        ).map(item => item.name);

        frozenModules.forEach(item => {
          if (!newVal.some((selectedItem: string) => selectedItem === item)) {
            newVal.unshift(item);
          }
        });
        this.selectedModules = newVal;
        updateModules(this.selectedModules);

      },
      deep: true
    }
  },
  beforeUnmount() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
    }
  }
}
</script>
