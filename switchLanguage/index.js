const base = require('../../utils/language.js')
const _ = base._

Component({
    data: {
        index: 0,
        language: 'zh_CN',
        array: [
            {
                value: 'zh_CN',
                name: _('简体中文')
            },
            {
                value: 'zh_TW',
                name: _('繁体中文')
            },
            {
                value: 'en',
                name: _('英文')
            }
        ]
    },
    lifetimes: {
        attached() {
            const language = base.getLanguage()
            let index = 0
            switch (language) {
                case 'zh_CN':
                    index = 0
                    break
                case 'zh_TW':
                    index = 1
                    break
                case 'en':
                    index = 2
                    break
                default:
                    break
            }
            this.setData({
                index: index,
                language: language,
                array: [
                    {
                        value: 'zh_CN',
                        name: _('简体中文')
                    },
                    {
                        value: 'zh_TW',
                        name: _('繁体中文')
                    },
                    {
                        value: 'en',
                        name: _('英文')
                    }
                ]
            })
        }
    },
    methods: {
        bindPickerChange: function (e) {
            this.setData({
                index: e.detail.value,
                language: this.data.array[e.detail.value].value
            })
            this.switchLanguage()
        },
        switchLanguage() {
            wx.setStorageSync('language', this.data.language)
            // 重新加载一次页面
            // wx.navigateTo({
            //     url: 'index'
            // })
            this.setData({
                array: [
                    {
                        value: 'zh_CN',
                        name: _('简体中文')
                    },
                    {
                        value: 'zh_TW',
                        name: _('繁体中文')
                    },
                    {
                        value: 'en',
                        name: _('英文')
                    }
                ]
            })

            // 触发页面刷新，否则当前页语言版本无法更新
            this.triggerEvent('refleshevent')
        }
    }
})
