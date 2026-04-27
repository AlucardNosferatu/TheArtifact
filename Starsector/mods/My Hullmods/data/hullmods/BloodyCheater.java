package data.hullmods;

import com.fs.starfarer.api.combat.BaseHullMod;
import com.fs.starfarer.api.combat.MutableShipStatsAPI;
import com.fs.starfarer.api.combat.ShipAPI;
import com.fs.starfarer.api.combat.ShipAPI.HullSize;


public class BloodyCheater extends BaseHullMod {
    // ==================== Cheating / Overpowered Effects ====================
    private static final float WEAPON_DAMAGE_BONUS = 200f; // Weapon damage +100%
    private static final float WEAPON_RANGE_BONUS = 200f; //
    private static final float BALLISTIC_ROF_BONUS = 200f; //
    private static final float ARMOR_BONUS = 400f; // Armor +200
    private static final float MAX_SPEED_BONUS = 100f; // Max speed +50%
    private static final float FLUX_CAPACITY_BONUS = 600f; // Flux capacity +300%
    private static final float FLUX_DISSIPATION_BONUS = 600f; // Flux dissipation +300%
    private static final float CREW_LOSS_REDUCTION = 90f; // Crew loss reduced by 90%
    private static final float SHIELD_DAMAGE_REDUCTION = 90f; //
    public static final float TURN_RATE_BONUS = 200f;       // 最大转向速度 +200%
    public static final float TURN_ACCEL_BONUS = 200f;      // 转向加速度 +200%

    @Override
    public void applyEffectsBeforeShipCreation(HullSize hullSize,
        MutableShipStatsAPI stats, String id) {
        // Weapon damage multiplier
        stats.getBallisticWeaponDamageMult()
             .modifyMult(id, 1f + (WEAPON_DAMAGE_BONUS / 100f));
        stats.getEnergyWeaponDamageMult()
             .modifyMult(id, 1f + (WEAPON_DAMAGE_BONUS / 100f));
        stats.getMissileWeaponDamageMult()
             .modifyMult(id, 1f + (WEAPON_DAMAGE_BONUS / 100f));

        // Armor bonus
        stats.getArmorBonus().modifyFlat(id, ARMOR_BONUS);

        // Speed bonus
        stats.getMaxSpeed().modifyPercent(id, MAX_SPEED_BONUS);

        // Flux bonuses
        stats.getFluxCapacity().modifyPercent(id, FLUX_CAPACITY_BONUS);
        stats.getFluxDissipation().modifyPercent(id, FLUX_DISSIPATION_BONUS);

        // Reduce crew losses
        stats.getCrewLossMult().modifyMult(id, 1f -
            (CREW_LOSS_REDUCTION / 100f));

        // You can add more crazy effects here, for example:
        stats.getShieldDamageTakenMult()
             .modifyMult(id, 1f - (SHIELD_DAMAGE_REDUCTION / 100f)); // Take only 10% shield damage
        // 武器射程加成（所有武器 +200%）
        stats.getWeaponRangeThreshold().modifyFlat(id, 0f);                    // 阈值设为0（让加成从头开始生效）
        stats.getWeaponRangeMultPastThreshold().modifyPercent(id, WEAPON_RANGE_BONUS);
        stats.getBallisticRoFMult().modifyPercent(id, BALLISTIC_ROF_BONUS); // Ballistic rate of fire +200%

        // 转向速度（船体本身）
        stats.getMaxTurnRate().modifyPercent(id, TURN_RATE_BONUS);
        stats.getTurnAcceleration().modifyPercent(id, TURN_ACCEL_BONUS);

        // 武器炮塔转速（可选，也加上更“作弊”）
        stats.getWeaponTurnRateBonus().modifyPercent(id, TURN_RATE_BONUS);
        stats.getBeamWeaponTurnRateBonus().modifyPercent(id, TURN_RATE_BONUS);
    }

    // Description parameters (replaces %s in order)
    @Override
    public String getDescriptionParam(int index, ShipAPI.HullSize hullSize) {
        if (index == 0) {
            return (int) WEAPON_DAMAGE_BONUS + "%";
        }

        if (index == 1) {
            return (int) ARMOR_BONUS + "";
        }

        if (index == 2) {
            return (int) MAX_SPEED_BONUS + "%";
        }

        if (index == 3) {
            return (int) FLUX_CAPACITY_BONUS + "%";
        }

        if (index == 4) {
            return (int) FLUX_DISSIPATION_BONUS + "%";
        }

        if (index == 5) {
            return (int) CREW_LOSS_REDUCTION + "%";
        }

        return null;
    }

    // Can this hullmod be installed on the ship?
    @Override
    public boolean isApplicableToShip(ShipAPI ship) {
        return true; // Currently allows all ships
    }

    // Reason shown when it cannot be installed
    @Override
    public String getUnapplicableReason(ShipAPI ship) {
        return "This hullmod is too overpowered for any ship!";
    }

    // Optional: text shown when uninstalling
    @Override
    public String getUninstallEffectDescription() {
        return "Removed this ridiculously overpowered hullmod...";
    }
}
