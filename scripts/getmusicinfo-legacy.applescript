if application "iTunes" is not running then
	return "STOPPED"
else
	try
		tell application "iTunes"
			set playerstate to player state
			
			if playerstate is not playing and playerstate is not paused then
				return "STOPPED"
			else
				if playerstate is playing then
					return "PLAYING\\" & name of current track & "\\" & artist of current track & "\\" & album of current track
				else
					return "PAUSED\\" & name of current track & "\\" & artist of current track & "\\" & album of current track
				end if
			end if
		end tell
	on error
		return "STOPPED"
	end try
end if