on run argv

	tell application "Finder" to set current_path to (POSIX path of (container of (path to me) as alias))

	tell application "Daily"

	set Today to (current date) - (item 1 of argv * days)

	print json with report "summary" from Today to Today with duration format "hours" with time rounding

	end tell

end run
