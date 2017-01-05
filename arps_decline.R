# Arps decline mock production generator
# (c) 2016 Derrick W. Turk | terminus data science, LLC

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

library(aRpsDCA)

first.names <- c(
  "Cedric",
  "Sanda",
  "King",
  "Iraida",
  "Cordell",
  "Barney",
  "Roseline",
  "Rodrigo",
  "Antonette",
  "Veta",
  "Christie",
  "Elvis",
  "Carlyn",
  "Deeann",
  "Edna",
  "Lyndsay",
  "Perry",
  "Sanjuanita",
  "Dominga",
  "Patsy"
)

last.names <- c(
  "Lamarre",
  "Maddy",
  "Chaney",
  "Hilson",
  "Nold",
  "Parkerson",
  "Schofield",
  "Nemeth",
  "Nevers",
  "Hanby",
  "Ravenscroft",
  "Grant",
  "Joye",
  "Mencer",
  "Gauer",
  "Smedley",
  "Hickman",
  "Northam",
  "Smyers",
  "Caron"
)

generate.name <- function (n)
{
    names <- paste(sample(first.names, n, replace=TRUE),
      sample(last.names, n, replace=TRUE))
    which.ranch <- sample(length(names), floor(n / 5))
    which.estate <- sample(length(names), floor(n / 5))
    which.estate <- setdiff(which.estate, which.ranch)
    names[which.ranch] <- paste(names[which.ranch], "Ranch")
    names[which.estate] <- paste(names[which.estate], "Estate")
    names
}

generate.base.decline <- function (n)
{
    qi <- rlnorm(n, 5.75, 0.75) # [unit] / day
    Di <- as.nominal(runif(n, 0.70, 0.98),
      from.period="year", to.period="day") # / year
    b <- runif(n, 1.1, 2.0)
    Df <- as.nominal(runif(n, 0.03, 0.20),
      from.period="year", to.period="day")
    lapply(seq_len(n), function (i) {
        arps.decline(qi[i], Di[i], b[i], Df[i])
    })
}

generate.production <- function (base.decline, time,
  buildup.time, buildup.initial.scalar,
  noise.sd.scalar,
  n.down, downtime.length.mean, downtime.length.sd,
  downtime.q.mean, downtime.q.sd)
{
    rate <- arps.q(base.decline, time)
    if (buildup.time > 0) {
        peak.rate <- arps.q(base.decline, buildup.time)
        rate[time < buildup.time] <-
          (peak.rate * (1.0 - buildup.initial.scalar) / buildup.time) *
            time[time < buildup.time] +
          buildup.initial.scalar * peak.rate
    }

    rate <- rate + rnorm(mean=0, sd=mean(rate) * noise.sd.scalar,
      n=length(rate))
    rate[rate < 0] <- 0

    if (n.down > 0) {
        down.begin <- sort(runif(min=buildup.time, max=max(time), n=n.down))
        down.time <- rnorm(mean=downtime.length.mean, sd=downtime.length.sd,
          n=n.down)
        down.end <- down.begin + down.time
        down.end[down.end > time[length(time)]] <- time[length(time)]
        i <- 1
        while (i < length(down.begin)) {
            if (down.end[i] > down.begin[i + 1])
                down.end[i] <- down.begin[i] + # fallback: 75% of begin-to-begin
                  (down.begin[i + 1] - down.begin[i]) * 0.75
            i <- i + 1
        }
        sapply(seq_along(down.begin), function (i) {
            which.down <- (time >= down.begin[i] & time <= down.end[i])
            rate[which.down] <<- rnorm(mean=downtime.q.mean, sd=downtime.q.sd,
              n=sum(which.down))
        })
        rate[rate < 0] <- 0
    }

    rate
}

generate.data <- function (n)
{
    well.names <- paste0(generate.name(n), " #",
      sample(23, n, replace=TRUE), "H")
    base.declines <- generate.base.decline(n)
    production <- lapply(base.declines, function (decl) {
        # daily data for 6 months to 2 years
        production.time <- seq(0, sample(seq(6 * 30, 2 * 365), 1))
        production.rate <- generate.production(decl, production.time,
          runif(1, 15, 60), # buildup time
          runif(1, 0.1, 0.4), # buildup initial fraction
          0.04, # noise SD fraction
          sample(5, 1) - 1, # number of downtimes
          runif(1, 5, 15), # downtime mean length (days)
          3, # downtime length SD (days)
          decl$qi * 0.10, # downtime average rate 
          decl$qi * 0.02) # downtime rate SD
        list(time=production.time, rate=production.rate)
    })
    do.call(rbind, lapply(seq_along(well.names), function (i) {
        data.frame(
          well.name=well.names[i],
          time=production[[i]]$time,
          rate=production[[i]]$rate)
    }))
}
