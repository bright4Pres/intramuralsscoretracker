function $(selectors) {
    return document.querySelector(selectors)
}

function $$(selectors) {
    return Array.from(document.querySelectorAll(selectors))
}

function getElements(teamList) {
    const marqueeText = $('.marquee__text')

    const teams = teamList.reduce((teams, team) => {
        teams[team.name] = $(`.points__team--${team.name}`)
        return teams
    }, {})

    return {
        marqueeText,
        teams,
    }
}

class Main {
    elements = {}
    teamList = []
    teamMap = {}
    winner = null
    lastScores = {}

    constructor(teamMap) {
        console.debug('constructor', teamMap)

        this.teamMap = teamMap ?? {}
        this.teamList = Object.values(this.teamMap)
        this.elements = getElements(this.teamList)
        
        // Store initial scores
        this.teamList.forEach(team => {
            this.lastScores[team.name] = team.points
        })
        
        // Start polling for score updates
        this.startPolling()
    }

    startPolling() {
        // Poll every 2 seconds for score updates
        setInterval(() => {
            this.fetchScores()
        }, 2000)
    }

    async fetchScores() {
        try {
            const response = await fetch('/api/scores/')
            const teams = await response.json()
            
            teams.forEach(team => {
                const oldScore = this.lastScores[team.name]
                const newScore = team.points
                
                if (newScore > oldScore) {
                    // Score increased - animate
                    const pointsScored = newScore - oldScore
                    this.teamMap[team.name].points = newScore
                    this.lastScores[team.name] = newScore
                    this.animate(this.teamMap[team.name], pointsScored)
                } else if (newScore !== oldScore) {
                    // Score changed but didn't increase (reset)
                    this.teamMap[team.name].points = newScore
                    this.lastScores[team.name] = newScore
                    this.elements.teams[team.name].textContent = newScore
                }
            })
        } catch (error) {
            console.error('Error fetching scores:', error)
        }
    }

    async animate(team, pointsScored) {
        console.debug('update', team, pointsScored)

        // Expand the scoring team's quadrant
        const quadrant = $(`.points__quadrant--${team.name}`)
        quadrant.classList.add('expanded')
        quadrant.style.backgroundColor = team.colorAsHex

        // Set marquee text and shadow color
        const marqueeText = $('.marquee__text')
        const teamDisplayName = team.name.charAt(0).toUpperCase() + team.name.slice(1)
        marqueeText.textContent = `${teamDisplayName} scored ${pointsScored} point${pointsScored !== 1 ? 's' : ''}!`
        marqueeText.style.color = 'white'
        marqueeText.style.textShadow = `0 0 20px ${team.colorAsHex}, 0 0 40px ${team.colorAsHex}, 0 0 60px ${team.colorAsHex}, 0 4px 8px rgba(0,0,0,0.8)`

        const random = (min, max) => {
            min = Math.ceil(min)
            max = Math.floor(max)
            return Math.floor(Math.random() * (max - min + 1) + min)
        }

        const shoot = (angle, scalar) => {
            confetti({
                particleCount: random(5, 10),
                angle: random(angle - 5, angle + 5),
                spread: random(35, 55),
                startVelocity: random(35, 55),
                colors: ['#FFFFFF', team.colorAsHex, team.colorAsHex],
                scalar,
            })
        }

        for (let index = 0; index < 9; index++) {
            setTimeout(shoot, random(0, 200), index * 22.5, random(28, 32) / 10)

            setTimeout(
                shoot,
                random(100, 300),
                index * 22.5,
                random(18, 22) / 10,
            )
        }

        document.documentElement.classList.add('goal', `goal--${team.name}`)

        if (team.points === 10) {
            document.documentElement.classList.add('win', `win--${team.name}`)
        }

        setTimeout(() => {
            this.elements.teams[team.name].textContent = team.points
        }, 150)

        await new Promise((resolve) => {
            this.elements.marqueeText.addEventListener('animationend', resolve, { once: true })
        })

        // Remove expansion and reset background
        quadrant.classList.remove('expanded')
        quadrant.style.backgroundColor = ''

        document.documentElement.classList.remove('goal', `goal--${team.name}`)
    }
}

// Initialize with team data from the database
async function initializeApp() {
    try {
        const response = await fetch('/api/scores/')
        const teams = await response.json()
        
        const teamMap = {}
        teams.forEach(team => {
            teamMap[team.name] = {
                name: team.name,
                points: team.points,
                colorAsHex: team.color
            }
        })
        
        const main = new Main(teamMap)
        window.main = main // Make it globally accessible
    } catch (error) {
        console.error('Error initializing app:', error)
        // Fallback to default team map if API fails
        const defaultTeamMap = {
            shinobi: { name: 'shinobi', points: 0, colorAsHex: '#8B4789' },
            pegasus: { name: 'pegasus', points: 0, colorAsHex: '#3498DB' },
            chimera: { name: 'chimera', points: 0, colorAsHex: '#E74C3C' },
            phoenix: { name: 'phoenix', points: 0, colorAsHex: '#F39C12' }
        }
        const main = new Main(defaultTeamMap)
        window.main = main
    }
}

// Start the app
initializeApp()