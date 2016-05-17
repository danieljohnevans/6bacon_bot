#!/usr/bin/env ruby

require 'httparty'
require 'bundler/setup'
require 'json'
require 'rubygems'
require 'twitter'

$client = Twitter::REST::Client.new do |config|
    config.consumer_key          = "YOUR_CONSUMER_KEY"
    config.consumer_secret       = "YOUR_CONSUMER_SECRET"
    config.access_token          = "YOUR_ACCESS_TOKEN"
    config.access_token_secret   = "YOUR_ACCESS_TOKEN_SECRET"
end

## Generate a random id and lookup via relationship and people urls

randos = Hash.new( rand(100000000..100200719) )

class Randomizer
    include HTTParty
    format :json

    def self.find_by_id(id)
        get("http://www.sixdegreesoffrancisbacon.com/relationships/#{id}.json", :query=> {:id => id, :output => "json"})
    end

end

class Personalizer
    include HTTParty
    format :json

    def self.find_by_id(num)
        get("http://www.sixdegreesoffrancisbacon.com/people/#{num}.json", :query=> {:num => num, :output => "json"})
    end

end

## Create hashes that reference various JSON objects. NB: Randomizer pulls from relationship url, Personalizer pulls from people URL.

rel_id = Hash.new( Randomizer.find_by_id("#{randos[2]}").parsed_response{0}["id"] )
p1 = Hash.new(Randomizer.find_by_id("#{randos[2]}").parsed_response{0}["person1_index"] )
p2 = Hash.new(Randomizer.find_by_id("#{randos[2]}").parsed_response{0}["person2_index"] )

hash = Hash.new("Go Fish")
hash["rel"] = Randomizer.find_by_id("#{randos[2]}").parsed_response{0}["type_certainty_list"]

## Pulls from person id and outputs person information

hesh = Hash.new("Go Fish")
hesh["person1"] = Personalizer.find_by_id("#{p1[2]}").parsed_response{0}["display_name"]
hesh["person2"] = Personalizer.find_by_id("#{p2[2]}").parsed_response{0}["display_name"]
hesh["hist1"] = Personalizer.find_by_id("#{p1[2]}").parsed_response{0}["historical_significance"]
hesh["hist2"] = Personalizer.find_by_id("#{p2[2]}").parsed_response{0}["historical_significance"]
hesh["by1"] = Personalizer.find_by_id("#{p1[2]}").parsed_response{0}["ext_birth_year"]
hesh["by2"] = Personalizer.find_by_id("#{p2[2]}").parsed_response{0}["ext_birth_year"]
hesh["dy1"] = Personalizer.find_by_id("#{p1[2]}").parsed_response{0}["ext_death_year"]
hesh["dy2"] = Personalizer.find_by_id("#{p2[2]}").parsed_response{0}["ext_death_year"]
hesh["by1_T"] = Personalizer.find_by_id("#{p1[2]}").parsed_response{0}["birth_year_type"]
hesh["by2_T"] = Personalizer.find_by_id("#{p2[2]}").parsed_response{0}["birth_year_type"]
hesh["dy1_T"] = Personalizer.find_by_id("#{p1[2]}").parsed_response{0}["death_year_type"]
hesh["dy2_T"] = Personalizer.find_by_id("#{p2[2]}").parsed_response{0}["death_year_type"]

##six modifiers (“AF” “BF” “CA” “IN” “AF/IN” “BF/IN”) 
##which are abbreviations for (“after” “before” “circa” “in” “after or in” and “before or in”). 

replacements = [ ["AF", "after"], ["BF", "before"], ["CA", "circa"], ["IN", "in"], ["AF/IN", "after or in"], 
    ["BF/IN", "before or in"] ]
replacements.each {|replacement| hesh["by1_T"].gsub!(replacement[0], replacement[1])}

replacements = [ ["AF", "after"], ["BF", "before"], ["CA", "circa"], ["IN", "in"], ["AF/IN", "after or in"], 
    ["BF/IN", "before or in"] ]
replacements.each {|replacement| hesh["by2_T"].gsub!(replacement[0], replacement[1])}

replacements = [ ["AF", "after"], ["BF", "before"], ["CA", "circa"], ["IN", "in"], ["AF/IN", "after or in"], 
    ["BF/IN", "before or in"] ]
replacements.each {|replacement| hesh["dy1_T"].gsub!(replacement[0], replacement[1])}

replacements = [ ["AF", "after"], ["BF", "before"], ["CA", "circa"], ["IN", "in"], ["AF/IN", "after or in"], 
    ["BF/IN", "before or in"] ]
replacements.each {|replacement| hesh["dy2_T"].gsub!(replacement[0], replacement[1])}


## Construct tweets and pull from hashes / heshes

option = Hash.new( "The @6bacon community is " + hash["rel"][0][1].floor.to_s + "% certain that " + hesh["person1"] + " " + 
    hash["rel"][0][2].downcase + " " + hesh["person2"] + ": http://www.sixdegreesoffrancisbacon.com/relationships/#{rel_id[0]}" )

option1 = Hash.new( "The @6bacon community is " + hash["rel"][0][1].floor.to_s + "% certain that " + hesh["person1"] + " was " + 
    hash["rel"][0][2].downcase + " " + hesh["person2"] + ": http://www.sixdegreesoffrancisbacon.com/relationships/#{rel_id[0]}" )

option2 = Hash.new( "The @6bacon community is " + hash["rel"][0][1].floor.to_s + "% certain that " + hesh["person1"] + " was a " + 
    hash["rel"][0][2].downcase + " " + hesh["person2"] + ": http://www.sixdegreesoffrancisbacon.com/relationships/#{rel_id[0]}" )

option3 = Hash.new( "The @6bacon community is " + hash["rel"][0][1].floor.to_s + "% certain that " + hesh["person1"] + " was an " + 
    hash["rel"][0][2].downcase + " " + hesh["person2"] + ": http://www.sixdegreesoffrancisbacon.com/relationships/#{rel_id[0]}" )

h = Hash.new("I am a bot. Please see more at : www.sixdegreesoffrancisbacon.com/")
h["who1"] = ( hesh["person1"] + ", " + hesh["hist1"] + ", was born " + hesh["by1_T"] + " " + hesh["by1"].to_s + 
    " and died " + hesh["dy1_T"] + " " + hesh["dy1"].to_s + ": http://www.sixdegreesoffrancisbacon.com/people/#{p1[0]}" )
h["who2"] = ( hesh["person2"] + ", " + hesh["hist2"] + ", was born " + hesh["by2_T"] + " " + hesh["by2"].to_s + 
    " and died " + hesh["dy2_T"] + " " + hesh["dy2"].to_s + ": http://www.sixdegreesoffrancisbacon.com/people/#{p2[0]}" )

h["who3"] = ("I was built by @djohnevans at Carnegie Mellon University in May of 2016")

## Write statement dictionary for various relationship types, save in method, and post to twitter.

def do_something(data)
    $client.update("#{data}")
    sleep(1.0/8.0)
end

hash["rel"].each do |key, value|
  if key == 4 or 5 or 9 or 50
    do_something("#{option[2]}")
elsif key == 8 or 40 or 43 or 44 or 45
    do_something("#{option1[2]}")
elsif key == 2 or 6 or 7 or 10 or 11 or 12 or 14 or 15 or 16 or 17 or 18 or 19 or 20 or 21 or 22 or 23 or 
    24 or 25 or 26 or 27 or 28 or 29 or 30 or 31 or 32 or 33 or 34 or 35 or 36 or 37 or 38 or 42 or 46 or 47 or 48 or 51
    do_something("#{option2[2]}")
elsif key == 1 or 3 or 13 or 39 or 41 or 49
    do_something("#{option3[2]}")
  end
end

## Response options and post to twitter

$client.user_timeline("@6Bacon_Bot").take(1).each do |tweet|
  puts "#{tweet.user.screen_name}: #{tweet.text}"
  $client.update("#{h["who1"]}", in_reply_to_status_id: tweet.id)
  $client.update("#{h["who2"]}", in_reply_to_status_id: tweet.id)
end

puts "#{h["who1"]}"
puts "#{h["who2"]}"

